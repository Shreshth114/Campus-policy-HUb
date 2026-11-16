"""Aggregate completed retrieval observations without treating provider failures as misses."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def metrics(rows):
    n=len(rows)
    ranks=[next((i for i,r in enumerate(row,1) if r['gold']),None) for row in rows]
    return {'n':n,**{f'recall_at_{k}':sum(rank is not None and rank<=k for rank in ranks)/n if n else None for k in (1,3,5)},'mrr':sum(1/r if r else 0 for r in ranks)/n if n else None,'hits_at_3':sum(r is not None and r<=3 for r in ranks)}

def summarize(split):
    files=sorted((ROOT/'results'/split).glob('query-*.json'))
    data=[json.loads(p.read_text()) for p in files]
    result={}
    if not data:return {}
    for mode in data[0]['result']['rankings']:
        rows=[r['result']['rankings'][mode] for r in data]
        result[mode]={'overall':metrics(rows),'by_type':{kind:metrics([r['result']['rankings'][mode] for r in data if r['question']['type']==kind]) for kind in sorted({r['question']['type'] for r in data})}}
    # Sweep fixed cutoffs on tune only. No threshold selection from hold-out.
    if split=='tune':
        for mode in ('hyde_v2_prompt','avg_1_1','avg_1_2','avg_2_1'):
            for tau in (.35,.4,.45,.5,.55,.6,.65,.7):
                rows=[r['result']['rankings']['raw'] if r['result']['rankings']['raw'][0]['score']>=tau else r['result']['rankings'][mode] for r in data]
                result[f'routed_{mode}_{tau}']={'overall':metrics(rows),'raw_only_count':sum(r['result']['rankings']['raw'][0]['score']>=tau for r in data)}
    (ROOT/'results'/split/'summary.json').write_text(json.dumps(result,indent=2))
    print(split,'completed',len(data),'best',sorted([(name,v['overall']['mrr']) for name,v in result.items()],key=lambda r:r[1],reverse=True)[:8])
    return result

if __name__=='__main__':
    summarize('tune');summarize('holdout')
