"""Render recorded observations only; never invoke retrieval or a provider."""
import json,sys
from pathlib import Path

def render(folder):
    folder=Path(folder);meta=json.loads((folder/'metadata.json').read_text())
    lines=['# Actual PS1 diagnostic execution','',f"Run status: {meta['status']}",'','Real provider requests; disposable index built from the actual PDF. Three diagnostic questions, each run through Raw, HyDE and Fusion. Draft labels remain unverified: this report contains no scored accuracy or winner claim. Answer caching and HyDE caching disabled. Embedding-model loading/index setup occur before query timings. Raw/HyDE/Fusion do not necessarily receive identical generated search keys because caching is disabled.','', '| Case | Mode | Decision | Reason | Provider/model | Retrieved blocks | Elapsed s |','|---|---|---|---|---|---:|---:|']
    records=[]
    for path in sorted(folder.glob('ps1-*.json')):
        r=json.loads(path.read_text());t=r.get('trace',{});calls=r.get('provider_calls',[])
        model='; '.join(dict.fromkeys(str(c.get('response',{}).get('provider',''))+'/'+str(c.get('response',{}).get('model','')) for c in calls))
        lines.append(f"| {r['question']['id']} | {r['mode']} | {t.get('decision','error')} | {t.get('abstain_reason') or t.get('error') or r.get('error') or '—'} | {model or 'none'} | {len(t.get('retrieved',[]))} | {r.get('elapsed_s',0):.2f} |")
        records.append((path,r))
    for path,r in records:
        t=r.get('trace',{})
        lines += ['',f"## {r['question']['id']} / {r['mode']}",'',r['question']['query'],'',f"Full machine-readable record: [{path.name}]({path.name})",'', '### Application output','',t.get('answer') or 'No application answer recorded.','', '### Actual generation and errors']
        for i,c in enumerate(r.get('provider_calls',[]),1):
            response=c.get('response',{})
            lines += ['',f"Call {i}: {response.get('provider','unavailable')} / {response.get('model','unavailable')}",'','```text',response.get('text') or json.dumps(c.get('error',{}),indent=2),'```']
        lines += ['','### Validator failures','', '```json',json.dumps(r.get('claim_failures',[]),indent=2),'```','','### Retrieved evidence']
        for rank,c in enumerate(t.get('retrieved',[]),1):
            lines += ['',f"Rank {rank}; chunk `{c['chunk_id']}`; page(s) {c.get('pages') or [c.get('page')]}; cosine {c.get('score')}; RRF {c.get('rrf_score')}",'','```text',c.get('text',''),'```','','Exact answer excerpt (if selected):','```text',c.get('answer_excerpt') or '[not selected / not sent]','```']
        lines += ['','Timings / usage:','```json',json.dumps({'timings_ms':t.get('timings_ms'), 'llm_usage':t.get('llm_usage'), 'warnings':t.get('warnings'), 'error':r.get('error') or t.get('error')},indent=2),'```']
    integrity=folder/'integrity.json'
    if integrity.exists():lines += ['','## Production integrity','', '```json',integrity.read_text(),'```']
    (folder/'REPORT.md').write_text('\n'.join(lines))
    print('Rendered',len(records),'actual observations:',folder/'REPORT.md')
if __name__=='__main__':render(sys.argv[1])
