"""Readiness gates never promote the real draft labels."""
from evaluation.ps1.refinements.freeze_manifest import readiness,sha
from tests.test_review_evaluation import case,human


def ready(tmp_path):
    docs=[]
    for i in range(2):
        p=tmp_path/f'fixture{i}.pdf';p.write_bytes(f'SYNTHETIC HASH FIXTURE {i}'.encode())
        docs.append({'id':str(i),'path':p.name,'sha256':sha(p),'institution':f'Synthetic {i}','layout_outcome':'answer_supported'})
    spec={'purpose':'heldout','human_exposure_attested':True,'documents':docs,'development_document_sha256':[],
          'modes':['raw','hyde','fusion'],'fallback_policy':'groq_only_no_provider_fallback','answer_cache':False,'hyde_cache':False}
    c=case();c['document_id']='0';h=human('a',True);h['source_pdf_checked']=True
    b=case('b');b['document_id']='1';hb=human('b',True);hb['source_pdf_checked']=True
    return spec,[c,b],[h,hb]


def test_pending_or_exposed_data_cannot_be_frozen(tmp_path):
    spec,cases,labels=ready(tmp_path)
    assert not readiness(spec,cases,labels,tmp_path)
    labels[0]['human_reviewed']=False
    assert readiness(spec,cases,labels,tmp_path)
    labels[0]['human_reviewed']=True
    spec['development_document_sha256']=[spec['documents'][0]['sha256']]
    assert any('exposed' in x for x in readiness(spec,cases,labels,tmp_path))


def test_hash_change_and_cache_policy_block_readiness(tmp_path):
    spec,cases,labels=ready(tmp_path);(tmp_path/'fixture0.pdf').write_bytes(b'changed')
    spec['answer_cache']=True
    errors=readiness(spec,cases,labels,tmp_path)
    assert any('hash mismatch' in x for x in errors) and any('caches disabled' in x for x in errors)


def test_freeze_is_write_once_and_detects_input_drift(tmp_path):
    import json,pytest
    from evaluation.ps1.refinements.freeze_manifest import freeze,verify
    spec,cases,labels=ready(tmp_path)
    spec.update(cases='cases.json',annotations='labels.json')
    (tmp_path/'cases.json').write_text(json.dumps(cases));(tmp_path/'labels.json').write_text(json.dumps(labels))
    spec_path=tmp_path/'spec.json';spec_path.write_text(json.dumps(spec));out=tmp_path/'frozen.json'
    freeze(spec_path,out)
    assert verify(spec_path,out)
    with pytest.raises(FileExistsError):freeze(spec_path,out)
    (tmp_path/'labels.json').write_text(json.dumps(labels)+'\n')
    with pytest.raises(ValueError,match='annotations changed'):verify(spec_path,out)
