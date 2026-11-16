"""Small real-provider diagnostic in disposable storage; never scores draft labels."""
import argparse, asyncio, hashlib, json, os, sys, tempfile, time
from dataclasses import asdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))

async def run(args):
    from src import institutions,store,personal,documents,pipeline,answer,hyde,llm
    from src.reindex import reindex
    from src.config import PROVIDERS,EMBED_MODEL,TOP_K,CONFIDENCE_THRESHOLD
    from src.evidence import claim_failures
    from src.answer import answer_evidence,validate_answer
    from src.store import RetrievedChunk
    rows=json.loads(Path(args.questions_file).read_text()) if args.questions_file else json.loads((Path(__file__).parent/'questions.draft.json').read_text())
    if args.questions_file and args.ids is None: args.ids=[r['id'] for r in rows]
    if args.ids is None: args.ids=['ps1-02','ps1-14','ps1-21']
    selected=[r for r in rows if r['id'] in args.ids]
    if len(selected)!=len(set(args.ids)):raise ValueError('Unknown or repeated question ID')
    output=Path(args.output);output.mkdir(parents=True,exist_ok=False)
    protected={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for d in ['data','.chroma','.chroma-institutions'] for p in (ROOT/d).rglob('*') if p.is_file()}
    credentials=[v.get('api_key','') for v in PROVIDERS.values()]+[os.getenv('ADMIN_API_TOKEN','')]
    capability=''
    def clean(value):
        if isinstance(value,dict):return {k:clean(v) for k,v in value.items() if k not in {'workspace_id','source_path'}}
        if isinstance(value,list):return [clean(v) for v in value]
        if isinstance(value,str):
            for secret in credentials+[capability]:
                if secret:value=value.replace(secret,'[REDACTED]')
        return value
    def save(name,value):
        (output/name).write_text(json.dumps(clean(value),indent=2,ensure_ascii=False))
    real_retrieve=pipeline.retrieve
    retrieval_records=[]
    async def observed_retrieve(*a,**kw):
        value=await real_retrieve(*a,**kw)
        retrieval_records.append(asdict(value))
        return value
    pipeline.retrieve=observed_retrieve
    # Instrument the existing unified client without replacing provider behavior.
    real=llm.get_llm_client()
    # User authorized Groq only for this diagnostic; change only this local client.
    if real.primary.name != 'groq':
        real.primary = llm.GroqProvider()
    class DisabledFallback:
        name = 'disabled_for_diagnostic'
        def is_configured(self): return False
    real.fallback = DisabledFallback()
    calls=[]
    class Capture:
        async def chat(self,**kwargs):
            item={'messages':kwargs['messages'],'max_tokens':kwargs.get('max_tokens'),'temperature':kwargs.get('temperature')};calls.append(item)
            try:
                response=await real.chat(**kwargs)
                item['response']=asdict(response)
                return response
            except Exception as exc:
                item['error']=llm.provider_error_details(exc,credentials)
                raise
    answer.get_llm_client=lambda:Capture()
    hyde.get_llm_client=lambda:Capture()
    save('metadata.json',{'status':'running','question_ids':args.ids,'modes':args.modes,'labels_verified':False,'evaluation':'diagnostic_subset_not_accuracy_benchmark','provider_policy':'groq_only_fallback_disabled','embedding_model':EMBED_MODEL,'top_k':TOP_K,'confidence_threshold':CONFIDENCE_THRESHOLD,'source_sha256':hashlib.sha256(Path(args.pdf).read_bytes()).hexdigest()})
    with tempfile.TemporaryDirectory(prefix='ps1-diagnostic-') as tmp:
        institutions.DATA_ROOT=Path(tmp)/'data';store.CHROMA_DIR=str(Path(tmp)/'chroma');store._client=None;store._collection=None
        entry=personal.create('Disposable actual-document diagnostic');capability=entry['workspace_id'];ctx=personal.resolve(capability)
        with institutions.scope(ctx):
            doc=documents.upload(Path(args.pdf).name,Path(args.pdf).read_bytes())
            report=await asyncio.to_thread(reindex)
            save('index_setup.json',report)
            if report['status']!='ok':raise RuntimeError('Disposable indexing failed')
            if args.questions_file:
                corpus=store.get_collection().get(where=ctx.filter,include=['documents','metadatas'])
                save('corpus.json',corpus)
                from evaluation.ps1.review_metrics import evidence_map
                save('evidence_mapping.json',evidence_map(selected,corpus))
            import importlib.metadata,platform
            from src import config,prompts
            save('frozen_settings.json',{'python':platform.python_version(),
                 'packages':{name:importlib.metadata.version(name) for name in ('fastembed','chromadb','onnxruntime','httpx')},
                 'source_code_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'src').glob('*.py')},
                 'prompts':{'hyde_system':prompts.HYDE_SYSTEM_PROMPT,'hyde_user':prompts.HYDE_USER_TEMPLATE,'answer_system':prompts.ANSWER_SYSTEM_PROMPT,'answer_user':prompts.ANSWER_USER_TEMPLATE,'answer_review':prompts.ANSWER_REVIEW_PROMPT},
                 'config':{k:getattr(config,k) for k in ('TOP_K','CONFIDENCE_THRESHOLD','ANSWER_MAX_TOKENS','ANSWER_CHUNKS_LIMIT','HYDE_MAX_TOKENS','CHUNK_MAX_TOKENS','CHUNK_OVERLAP_FRACTION','EMBED_MODEL')},
                 'label_sha256':hashlib.sha256(Path(args.questions_file).read_bytes()).hexdigest() if args.questions_file else None,
                 'provider':'groq','model':real.primary.model,'fallback':False,'mode_order':'cyclic' if args.balanced else 'fixed', 'pause_seconds':args.pause,
                 'budget_note':'source-size adaptive answer budget, cap 1200; Groq GPT-OSS low reasoning; RRF k=60'})
            for row_index,row in enumerate(selected):
                modes=args.modes[row_index%len(args.modes):]+args.modes[:row_index%len(args.modes)] if args.balanced else args.modes
                for mode in modes:
                    if args.pause:
                        await asyncio.sleep(args.pause)
                    retrieval_records.clear();calls.clear();token=hyde.cache_enabled.set(False);started=time.perf_counter()
                    print(f"START {row['id']} {mode}",flush=True)
                    try:
                        trace=await pipeline.ask(row['query'],mode,use_cache=False)
                        result={'question':row,'mode':mode,'trace':trace.to_dict(),'provider_calls':calls,'retrieval_before_merge':retrieval_records,'elapsed_s':time.perf_counter()-started}
                        # validate_answer failures appear in enabled diagnostics; capture
                        # exact messages/raw responses here even if rejected by pipeline.
                        answer_calls=[c for c in calls if c.get('response') and c['messages'][0]['content'].startswith('You are a university policy assistant')]
                        if answer_calls:
                            import html,re
                            from types import SimpleNamespace
                            from src.grounding import parse_object,render_contract
                            generation=answer_calls[-1]
                            text=generation['messages'][1]['content']
                            excerpts=[SimpleNamespace(text=html.unescape(re.sub(r'</?provision(?: id="P[1-9]\d*")?>','',x))) for x in re.findall(r'<excerpt[^>]*>\n(.*?)\n</excerpt>',text,re.S)]
                            raw=generation['response']['text']
                            contract=parse_object(raw)
                            proposed,contract_failures=render_contract(contract,excerpts)
                            result['raw_model_output']=raw
                            result['proposed_answer']=proposed
                            result['selection_failures']=contract_failures
                            canonical=answer.canonicalize_citations(proposed or '')
                            result['claim_failures']=claim_failures(canonical,excerpts) if proposed else []
                            from src.evidence import verify_quotes
                            verified,failed=verify_quotes(canonical,excerpts)
                            result['raw_quotation_attribution']={'verified':verified,'failed':failed}
                            result['coverage_reviews']=[c for c in calls if c['messages'][0]['content'].startswith('Review a proposed evidence selection')]
                        save(f"{row['id']}-{mode}.json",result)
                        print(f"DONE {row['id']} {mode}: {trace.decision}; {trace.abstain_reason}; {len(trace.retrieved)} blocks",flush=True)
                    except Exception as exc:
                        save(f"{row['id']}-{mode}.json",{'question':row,'mode':mode,'error':llm.provider_error_details(exc,credentials),'provider_calls':calls})
                        print(f"ERROR {row['id']} {mode}: {type(exc).__name__}",flush=True)
                    finally:hyde.cache_enabled.reset(token)
        if store._client is not None and hasattr(store._client,'close'):store._client.close()
    after={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for d in ['data','.chroma','.chroma-institutions'] for p in (ROOT/d).rglob('*') if p.is_file()}
    save('integrity.json',{'files_checked':len(protected),'byte_identical':protected==after})
    if protected!=after:raise RuntimeError('Production snapshot changed; inspect before attribution')
    meta=json.loads((output/'metadata.json').read_text());meta['status']='completed';save('metadata.json',meta)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--questions-file');p.add_argument('--balanced',action='store_true');p.add_argument('--modes',nargs='+',choices=['raw','hyde','fusion'],default=['raw','hyde','fusion']);p.add_argument('--pause',type=float,default=0);p.add_argument('--pdf',required=True);p.add_argument('--output',required=True);p.add_argument('--ids',nargs='+',default=None);args=p.parse_args();asyncio.run(run(args))
