"""Freeze reviewed unseen evaluation inputs; never approves or labels sources."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
from pathlib import Path
from evaluation.ps1.refinements.review_evaluation import human_label_complete,unique

ROOT=Path(__file__).resolve().parents[3]


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def known_development_sources():
    seen=set()
    for path in (ROOT/'evaluation/ps1/runs').glob('*/metadata.json'):
        try:
            record=json.loads(path.read_text())
        except (OSError,ValueError):continue
        digest=record.get('source_sha256')
        if isinstance(digest,str) and len(digest)==64:seen.add(digest)
    return seen


def source_snapshot():
    paths=list((ROOT/'src').glob('*.py'))+list((ROOT/'bench').glob('*.py'))+list((ROOT/'evaluation/ps1').rglob('*.py'))
    paths=[p for p in paths if 'runs' not in p.relative_to(ROOT).parts]
    return {str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)}


def readiness(spec,cases,annotations,base):
    errors=[]
    if spec.get('purpose')!='heldout' or spec.get('human_exposure_attested') is not True:
        errors.append('Unseen held-out provenance has not been attested')
    try:
        case_map=unique(cases,'id');labels=unique(annotations,'case_id')
    except (ValueError,KeyError):return ['Duplicate or missing case IDs']
    if not cases or set(case_map)!=set(labels):errors.append('Cases and annotations must match exactly')
    for cid in case_map:
        if not human_label_complete(labels.get(cid,{})) or labels.get(cid,{}).get('source_pdf_checked') is not True:
            errors.append('Human source adjudication pending: '+cid)
    docs=spec.get('documents',[]);seen=set(spec.get('development_document_sha256',[])) | known_development_sources()
    institutions={d.get('institution') for d in docs if d.get('institution')}
    if len(docs)<2 or len(institutions)<2:errors.append('Independent evaluation requires at least two institutions and PDFs')
    doc_map={d.get('id'):d for d in docs}
    if len(doc_map)!=len(docs) or None in doc_map:errors.append('Document IDs must be unique and present')
    hashes=[]
    for doc in docs:
        path=base/doc.get('path','')
        if not path.is_file():errors.append('Missing evaluation PDF: '+str(doc.get('id')));continue
        digest=sha(path);hashes.append(digest)
        if digest in seen:errors.append('Previously exposed document: '+str(doc.get('id')))
        if digest!=doc.get('sha256'):errors.append('Document hash mismatch: '+str(doc.get('id')))
        if doc.get('layout_outcome') not in ('answer_supported','extraction_abstention'):
            errors.append('Declare extraction/layout expectation: '+str(doc.get('id')))
    if len(set(hashes))!=len(hashes):errors.append('Duplicate document contents')
    used={doc_map.get(row.get('document_id'),{}).get('institution') for row in cases}
    if len(used-{None})<2:errors.append('Questions must cover at least two institutions')
    development_questions=set(spec.get('development_question_sha256',[]))
    for row in cases:
        if row.get('document_id') not in doc_map:errors.append('Unknown evaluation document: '+row['id'])
        qhash=hashlib.sha256(' '.join(row.get('question','').casefold().split()).encode()).hexdigest()
        if qhash in development_questions:errors.append('Previously revealed question: '+row['id'])
    if spec.get('modes')!=['raw','hyde','fusion'] or spec.get('fallback_policy')!='groq_only_no_provider_fallback':
        errors.append('Declare common Raw/HyDE/Fusion order and Groq-only provider policy')
    if spec.get('answer_cache') is not False or spec.get('hyde_cache') is not False:
        errors.append('Primary cold comparison requires both caches disabled')
    return errors


def freeze(spec_path,output):
    target=Path(output).resolve()
    if any(target.is_relative_to((ROOT/name).resolve()) for name in ('data','.chroma','.chroma-institutions')):
        raise ValueError('Freeze output cannot be written to production storage')
    spec_path=Path(spec_path).resolve();base=spec_path.parent;spec=json.loads(spec_path.read_text())
    cases_path=base/spec['cases'];labels_path=base/spec['annotations']
    cases=json.loads(cases_path.read_text());annotations=json.loads(labels_path.read_text())
    errors=readiness(spec,cases,annotations,base)
    if errors:raise ValueError('\n'.join(errors))
    from src import config
    from src.grounding import PROTOCOL
    settings={key:getattr(config,key) for key in ('TOP_K','CONFIDENCE_THRESHOLD','EMBED_MODEL','ANSWER_CHUNKS_LIMIT','ANSWER_MAX_TOKENS','HYDE_MAX_TOKENS','CHUNK_MAX_TOKENS','CHUNK_OVERLAP_FRACTION','LLM_TOTAL_WAIT_BUDGET')}
    manifest={'status':'frozen_inputs_not_executed','review_provenance':'user-attested human adjudication; software cannot authenticate reviewer identity',
              'protocol':PROTOCOL,'spec_sha256':sha(spec_path),'cases_sha256':sha(cases_path),'annotations_sha256':sha(labels_path),
              'documents':[{k:d[k] for k in ('id','institution','sha256','layout_outcome')} for d in spec['documents']],
              'source_sha256':source_snapshot(),
              'settings':settings,'provider':'groq','model':config.PROVIDERS['groq']['model'],'provider_fallback':False,
              'python':platform.python_version(),'packages':{p:importlib.metadata.version(p) for p in ('fastembed','onnxruntime','chromadb','httpx')},
              'modes':spec['modes'],'answer_cache':False,'hyde_cache':False,
              'limits':'Document/question hashes catch exact reuse only; human exposure attestation must also rule out paraphrase or tuning leakage. Freeze does not execute a benchmark. A diagnostic runner without these preflight checks is not the final benchmark runner.'}
    with Path(output).open('x') as stream:json.dump(manifest,stream,indent=2)
    return manifest


def verify(spec_path,manifest_path):
    """Fail on input/code drift; execution must call this before any queries."""
    path=Path(spec_path).resolve();base=path.parent;spec=json.loads(path.read_text());manifest=json.loads(Path(manifest_path).read_text())
    errors=[]
    if sha(path)!=manifest.get('spec_sha256'):errors.append('Evaluation specification changed')
    for field,key in [('cases','cases_sha256'),('annotations','annotations_sha256')]:
        if sha(base/spec[field])!=manifest.get(key):errors.append(field+' changed')
    errors+=readiness(spec,json.loads((base/spec['cases']).read_text()),json.loads((base/spec['annotations']).read_text()),base)
    if source_snapshot()!=manifest.get('source_sha256'):errors.append('Code inventory or contents changed')
    from src import config
    if {k:getattr(config,k) for k in manifest.get('settings',{})}!=manifest.get('settings'):errors.append('Runtime settings changed')
    if config.PROVIDERS['groq']['model']!=manifest.get('model'):errors.append('Model changed')
    if platform.python_version()!=manifest.get('python'):errors.append('Python changed')
    if any(importlib.metadata.version(k)!=v for k,v in manifest.get('packages',{}).items()):errors.append('Package versions changed')
    if errors:raise ValueError('\n'.join(errors))
    return True


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--spec',required=True);p.add_argument('--output');p.add_argument('--verify');args=p.parse_args()
    if args.verify:verify(args.spec,args.verify)
    elif args.output:freeze(args.spec,args.output)
    else:p.error('Use --output to freeze or --verify to check an existing manifest')
