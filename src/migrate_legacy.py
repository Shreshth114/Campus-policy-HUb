"""Explicit offline staged migration. Original legacy paths are never opened for writing."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import uuid
import numpy as np
from src.config import PROJECT_ROOT,EMBED_MODEL
from src import institutions,authority,store
from src.persistence import write_json

BASELINE=PROJECT_ROOT/'data/migrations/baseline'

def verify_inventory(base=BASELINE):
    inventory=json.loads((base/'inventory.json').read_text())
    for relative,digest in inventory.items():
        path=PROJECT_ROOT/relative
        if not path.is_file() or authority.source_hash(path)!=digest:
            raise ValueError(f'Legacy inventory changed: {relative}; cutover aborted')
    return inventory

def stage_records(ctx,entries,records,mapping):
    """Idempotent copy/upsert using persisted identities; safe to rerun after interruption."""
    with institutions.scope(ctx):
        registry={};manifest={};ids=[];metadatas=[];texts=[];vectors=[];chunks_map={}
        counts=Counter(m['doc_id'] for m in records['metadatas'] if not m.get('is_decoy'))
        for old_id,entry in entries.items():
            if entry['authority_status']!='pending': raise ValueError('Unexpected legacy approval state')
            source=Path(entry['source_path']);digest=authority.source_hash(source)
            if digest!=entry['file_hash']: raise ValueError('Source hash differs from registry')
            did=mapping['documents'][old_id]
            dest=ctx.raw/did.split(':')[-1]/digest/source.name;dest.parent.mkdir(parents=True,exist_ok=True)
            if dest.exists() and authority.source_hash(dest)!=digest: raise ValueError('Staging file hash mismatch')
            if not dest.exists(): shutil.copy2(source,dest)
            n=counts[old_id]
            values={k:v for k,v in entry.items() if k in authority.SourceEntry.__dataclass_fields__}
            values.update(doc_id=did,institution_id=ctx.institution_id,version_id=digest,original_filename=source.name,
                          source_path=str(dest),authority_status='pending',approved_at=None,history=[],
                          extraction_status='indexed' if n else 'failed',chunk_count=n,
                          extraction_error=None if n else 'No extractable text in legacy ingestion; see SOURCE_REVIEW.md')
            registry[did]=values
            if n:manifest[str(dest)]=digest
        for i,(cid,meta,text) in enumerate(zip(records['ids'],records['metadatas'],records['documents'])):
            decoy=bool(meta.get('is_decoy'));old_id=meta['doc_id']
            did=mapping['documents'].get(old_id,f'{ctx.institution_id}:evaluation:{old_id}')
            digest=meta['file_hash'];version=digest
            if not decoy and (old_id not in entries or digest!=entries[old_id]['file_hash']): raise ValueError('Vector ownership/hash mismatch')
            new_id=hashlib.sha256(f"{ctx.institution_id}|{did}|{version}|{meta['section']}|{meta['chunk_index']}".encode()).hexdigest()
            if new_id in ids: raise ValueError('Duplicate migrated chunk identity')
            new_meta={**meta,'doc_id':did,'institution_id':ctx.institution_id,'version_id':version,
                      'approved':False,'is_synthetic':decoy or bool(meta.get('is_synthetic'))}
            if not decoy:new_meta['source_path']=registry[did]['source_path']
            else:
                evaluation=ctx.path('decoys')/'legacy-decoy-vectors.json'
                new_meta['source_path']=str(evaluation)
            ids.append(new_id);metadatas.append(new_meta);texts.append(text);vectors.append(records['embeddings'][i]);chunks_map[cid]=new_id
        authority._save_registry(registry)
        store.upsert_chunks(ids,texts,vectors,metadatas)
        from src.reindex import _save_manifest
        _save_manifest(manifest)
        # Do not erase a cache on reruns; eligibility validation makes any stale entry unusable.
        if not ctx.path('cache').exists():write_json(ctx.path('cache'),[])
        if not ctx.path('hyde').exists():write_json(ctx.path('hyde'),{})
        evaluation=[{'id':cid,'text':t,'metadata':m,'embedding':list(v)} for cid,t,m,v in zip(ids,texts,metadatas,vectors) if m.get('is_decoy')]
        write_json(ctx.path('decoys')/'legacy-decoy-vectors.json',evaluation)
        stored=store.get_collection().get(where={'institution_id':ctx.institution_id},include=['documents','metadatas','embeddings'])
        if len(stored['ids'])!=len(ids) or set(stored['ids'])!=set(ids):raise ValueError('Staged vector count/identity mismatch')
        before={cid:(t,np.asarray(v,dtype=np.float32)) for cid,t,v in zip(ids,texts,vectors)}
        maximum_delta=0.
        for cid,t,v in zip(stored['ids'],stored['documents'],stored['embeddings']):
            original=before[cid][1]
            maximum_delta=max(maximum_delta,float(np.max(np.abs(v-original))))
            # Cosine collections normalize float32 vectors on insertion. Reuse the original
            # arrays as input and tolerate only observed float32 rounding, never new embeddings.
            if t!=before[cid][0] or not np.allclose(v,original,rtol=0,atol=1e-7): raise ValueError('Staged text/vector changed')
        return {'maximum_chroma_float32_delta':maximum_delta,'real_chunks':sum(not m.get('is_decoy') for m in metadatas),'decoy_chunks':len(evaluation),
                'sources':len(registry),'indexed_documents':sum(bool(n) for n in counts.values()),
                'failed_documents':sum(e['extraction_status']=='failed' for e in registry.values()),'chunk_mapping':chunks_map}

def migrate():
    verify_inventory()
    if (BASELINE/'mapping.json').exists():
        prior=json.loads((BASELINE/'mapping.json').read_text())
        if prior.get('stage')=='validated':return {**prior,'rerun':'already validated; no source status or data changed'}
    import chromadb
    from chromadb.config import Settings
    # Chroma may write bookkeeping even on get: inspect only a disposable copy of the backup.
    with tempfile.TemporaryDirectory(prefix='legacy-export-') as temp:
        shutil.copytree(BASELINE/'legacy/.chroma',Path(temp)/'chroma')
        client=chromadb.PersistentClient(path=str(Path(temp)/'chroma'),settings=Settings(anonymized_telemetry=False))
        records=client.get_collection('policy_chunks',embedding_function=None).get(include=['documents','metadatas','embeddings'])
    np.savez_compressed(BASELINE/'legacy_vectors.npz',ids=np.array(records['ids']),embeddings=records['embeddings'])
    entries=json.loads((BASELINE/'legacy/data/processed/source_registry.json').read_text())
    real=sum(not m.get('is_decoy') for m in records['metadatas']);decoys=len(records['ids'])-real
    actual=(len(list((PROJECT_ROOT/'data/raw').glob('*.pdf'))),len(entries),real,decoys)
    if actual!=(10,10,517,4):raise ValueError(f'Audited baseline discrepancy: {actual}; cutover aborted')
    if any(len(v)!=384 or not np.isfinite(v).all() for v in records['embeddings']):raise ValueError('Incompatible legacy vectors')
    state_path=BASELINE/'mapping.json'
    if state_path.exists():mapping=json.loads(state_path.read_text());ctx=institutions.resolve(mapping['institution_id'])
    else:
        if any(e['slug']=='msrit' for e in institutions.registry().values()):raise ValueError('Existing workspace without migration mapping; inspect ownership')
        institution=institutions.create_institution('Ramaiah Institute of Technology','msrit');ctx=institutions.resolve(institution['institution_id'])
        mapping={'institution_id':ctx.institution_id,'documents':{did:f'{ctx.institution_id}:{uuid.uuid4()}' for did in entries},'stage':'created'}
        write_json(state_path,mapping)
    # Evidence: recorded BGE ingestion configuration plus one recomputed excerpt per legacy document.
    if EMBED_MODEL!='BAAI/bge-small-en-v1.5':raise ValueError('Model differs from recorded legacy ingestion model')
    if not mapping.get('embedding_verified'):
        selected={}
        for i,m in enumerate(records['metadatas']):selected.setdefault(m['doc_id'],i)
        from src.embeddings import embed_texts
        indices=list(selected.values());checks=embed_texts([records['documents'][i] for i in indices])
        cosines=[float(np.dot(v,records['embeddings'][i])/(np.linalg.norm(v)*np.linalg.norm(records['embeddings'][i]))) for v,i in zip(checks,indices)]
        if len(cosines)!=len(indices) or min(cosines)<.99999:raise ValueError('Embedding compatibility not established; vector migration paused')
        mapping['embedding_verified']={'model':EMBED_MODEL,'dimensions':384,'sampled_documents':len(indices),'minimum_cosine':min(cosines),'method':'same-model recomputation per indexed document; vectors reused unchanged'}
        write_json(state_path,mapping)
    summary=stage_records(ctx,entries,records,mapping)
    queries=[]
    for line in (BASELINE/'legacy/bench/test_queries.jsonl').read_text().splitlines():
        if line.strip():
            q=json.loads(line);q.update(institution_id=ctx.institution_id,labels_verified=False)
            q['gold_chunk_ids']=[summary['chunk_mapping'].get(cid,cid) for cid in q.get('gold_chunk_ids',[])]
            queries.append(q)
    ctx.path('queries').write_text(''.join(json.dumps(q)+'\n' for q in queries))
    verify_inventory()
    with institutions.scope(ctx):
        if authority.approved_sources() or store.has_chunks():raise ValueError('Unexpected production eligibility')
    mapping.update(stage='validated',summary=summary);write_json(state_path,mapping)
    return {k:v for k,v in mapping.items() if k!='documents'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--execute',action='store_true',required=True);parser.parse_args()
    print(json.dumps(migrate(),indent=2))
