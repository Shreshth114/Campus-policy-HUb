"""Real Chroma indexing with temporary, explicitly synthetic marker documents."""
import importlib
import json
import pytest
from src import store, authority
from src.ingest import ingest_file

indexer = importlib.import_module('src.reindex')


@pytest.fixture
def corpus(monkeypatch):
    raw=indexer.DATA_RAW_DIR
    (raw/'alpha.txt').write_text('SYNTHETIC FIXTURE ALPHA. Marker alpha for indexing tests only. '*25)
    (raw/'beta.txt').write_text('SYNTHETIC FIXTURE BETA. Marker beta for indexing tests only. '*25)
    calls=[]
    def embed(texts):
        calls.extend(texts)
        return [[1.0,0.0] if 'ALPHA' in t else [0.0,1.0] for t in texts]
    monkeypatch.setattr(indexer,'embed_texts',embed)
    real=ingest_file
    monkeypatch.setattr(indexer,'ingest_file',lambda path,is_decoy=False:real(path,is_decoy,is_synthetic=True))
    return raw,calls


def test_add_noop_modify_delete_and_invalidation(corpus):
    from src.cache import cache_store,cache_lookup
    raw,calls=corpus
    first=indexer.reindex()
    assert first['status']=='ok' and first['chunks_added']>0
    initial=len(calls)
    assert indexer.reindex()['chunks_added']==0
    assert len(calls)==initial
    chunks=store.query([1.0,0.0],production=False,top_k=50)
    assert chunks and all(c.is_synthetic and not c.approved for c in chunks)
    assert store.query([1.0,0.0],production=True)==[]
    assert all(not authority.approve_source(cid) for cid in ('alpha','beta'))
    cache_store('fixture alpha','old answer',[chunks[0].chunk_id],[chunks[0].doc_id])
    (raw/'alpha.txt').write_text('SYNTHETIC FIXTURE ALPHA UPDATED. Freshness marker gamma. '*30)
    report=indexer.reindex()
    assert report['status']=='ok' and report['actions']['modified']==[str(raw/'alpha.txt')]
    assert report['cache_invalidated']==1
    assert all('ALPHA' in t for t in calls[initial:])
    assert cache_lookup('fixture alpha',production=False) is None
    assert any('UPDATED' in c.text for c in store.query([1.0,0.0],production=False,top_k=50))
    (raw/'beta.txt').unlink()
    report=indexer.reindex()
    assert report['chunks_deleted']>0
    assert all(c.doc_id!='beta' for c in store.query([0.0,1.0],production=False,top_k=50))


def test_embedding_failure_preserves_previous_chunks_and_manifest(corpus,monkeypatch):
    raw,_=corpus
    indexer.reindex()
    manifest=json.loads(indexer.MANIFEST_PATH.read_text())
    before=store.get_collection().get(include=['documents'])
    (raw/'alpha.txt').write_text('SYNTHETIC FIXTURE changed after previous successful indexing. '*20)
    def fail(_): raise RuntimeError('embedding fixture failure')
    monkeypatch.setattr(indexer,'embed_texts',fail)
    report=indexer.reindex()
    assert report['status']=='partial_failure'
    assert json.loads(indexer.MANIFEST_PATH.read_text())==manifest
    assert store.get_collection().get(include=['documents'])==before


def test_commit_failure_rolls_back_document(corpus,monkeypatch):
    raw,_=corpus
    indexer.reindex()
    before=store.get_collection().get(include=['documents'])
    (raw/'alpha.txt').write_text('SYNTHETIC FIXTURE ALPHA CHANGED. '*30)
    def fail(*args,**kw): raise RuntimeError('commit fixture failure')
    monkeypatch.setattr(indexer,'upsert_chunks',fail)
    report=indexer.reindex()
    assert report['status']=='partial_failure'
    after=store.get_collection().get(include=['documents'])
    assert dict(zip(after['ids'],after['documents']))==dict(zip(before['ids'],before['documents']))


def test_failed_new_file_is_retried(corpus,monkeypatch):
    raw,_=corpus
    empty=raw/'empty.txt'
    empty.write_text('')
    report=indexer.reindex()
    assert report['status']=='partial_failure'
    assert str(empty) not in indexer._load_manifest()
    empty.write_text('SYNTHETIC FIXTURE recovered extraction. '*30)
    assert indexer.reindex()['status']=='ok'
    assert str(empty) in indexer._load_manifest()


def test_decoy_filename_cannot_replace_source(corpus):
    _,_=corpus
    (indexer.DATA_DECOYS_DIR/'alpha.txt').write_text('SYNTHETIC DECOY FIXTURE. Never university evidence. '*30)
    assert indexer.reindex()['status']=='ok'
    records=store.get_collection().get(include=['metadatas'])
    ids={m['doc_id'] for m in records['metadatas']}
    assert len(ids)==3 and any(m['is_decoy'] for m in records['metadatas'])


def test_duplicate_source_stems_rejected_before_mutation(corpus):
    raw,_=corpus
    (raw/'alpha.pdf').write_bytes(b'SYNTHETIC invalid PDF fixture for collision detection only')
    report=indexer.reindex()
    assert report['status']=='partial_failure'
    assert len(authority.get_registry())==3
    assert len({e['doc_id'] for e in authority.get_registry().values()})==3


def test_keyboard_interrupt_during_embedding_preserves_state_and_retries(corpus,monkeypatch,capsys):
    raw,_=corpus
    indexer.reindex()
    manifest=indexer.MANIFEST_PATH.read_bytes()
    before=store.get_collection().get(include=['documents'])
    (raw/'alpha.txt').write_text('SYNTHETIC FIXTURE ALPHA updated for interruption testing. '*20)
    real_embed=indexer.embed_texts
    def interrupt(_): raise KeyboardInterrupt()
    monkeypatch.setattr(indexer,'embed_texts',interrupt)
    with pytest.raises(KeyboardInterrupt):
        indexer.reindex()
    assert indexer.MANIFEST_PATH.read_bytes()==manifest
    assert store.get_collection().get(include=['documents'])==before
    assert 'Interrupted during embedding' in capsys.readouterr().out
    monkeypatch.setattr(indexer,'embed_texts',real_embed)
    assert indexer.reindex()['status']=='ok'


def test_keyboard_interrupt_during_commit_restores_document(corpus,monkeypatch):
    raw,_=corpus
    indexer.reindex()
    manifest=indexer.MANIFEST_PATH.read_bytes()
    before=store.get_collection().get(include=['documents'])
    (raw/'alpha.txt').write_text('SYNTHETIC FIXTURE ALPHA changed before commit interruption. '*20)
    def interrupt(*args,**kwargs): raise KeyboardInterrupt()
    monkeypatch.setattr(indexer,'upsert_chunks',interrupt)
    with pytest.raises(KeyboardInterrupt):
        indexer.reindex()
    after=store.get_collection().get(include=['documents'])
    assert dict(zip(after['ids'],after['documents']))==dict(zip(before['ids'],before['documents']))
    assert indexer.MANIFEST_PATH.read_bytes()==manifest


def test_progress_reports_each_stage_and_document_timings(corpus,capsys):
    report=indexer.reindex()
    output=capsys.readouterr().out
    assert '[1/2]' in output and '[2/2]' in output
    assert 'Scan complete' in output and 'embedding finished' in output
    assert 'committing index update' in output and 'Manifest saved' in output
    assert 'Upserting chunks' in output
    assert all({'parse_chunk_s','embed_s','commit_s','persist_s','total_s'}<=set(doc['timings_s'])
               for doc in report['documents'])


def test_empty_document_reports_failure_without_manifest_success(corpus,capsys):
    raw,_=corpus
    empty=raw/'empty.txt'
    empty.write_text('')
    report=indexer.reindex()
    assert report['status']=='partial_failure'
    assert {'file':'empty.txt','stage':'parsing/chunking','error':'ValueError'} in report['errors']
    assert str(empty) not in indexer._load_manifest()
    assert 'empty.txt: FAILED' in capsys.readouterr().out


def test_keyboard_interrupt_during_delete_restores_document(corpus,monkeypatch):
    raw,_=corpus
    indexer.reindex()
    manifest=indexer.MANIFEST_PATH.read_bytes()
    before=store.get_collection().get(include=['documents'])
    (raw/'alpha.txt').write_text('SYNTHETIC FIXTURE ALPHA changed before deletion interruption. '*20)
    real_delete=indexer.delete_by_doc_id
    interrupted=False
    def interrupt_once(doc_id):
        nonlocal interrupted
        result=real_delete(doc_id)
        if not interrupted:
            interrupted=True
            raise KeyboardInterrupt()
        return result
    monkeypatch.setattr(indexer,'delete_by_doc_id',interrupt_once)
    with pytest.raises(KeyboardInterrupt):
        indexer.reindex()
    after=store.get_collection().get(include=['documents'])
    assert dict(zip(after['ids'],after['documents']))==dict(zip(before['ids'],before['documents']))
    assert indexer.MANIFEST_PATH.read_bytes()==manifest
