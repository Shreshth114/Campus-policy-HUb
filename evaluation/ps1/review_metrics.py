"""Mechanical evidence metrics; never manufacture semantic or human labels."""
import json,re,statistics,unicodedata,math
from pathlib import Path


def norm(text):
    text=re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',text or '')
    return ' '.join(unicodedata.normalize('NFKC',text).casefold().split())


def evidence_map(rows,corpus):
    mapping={}
    for row in rows:
        groups=[]
        for group in row['source_groups']:
            # Split a source group into complete source sentences. Alternatives
            # are interchangeable chunks for one sentence, not all mandatory IDs.
            text=re.sub(r'^B\d+(?:\.\d+)*\.?\s*','',group['quote'])
            for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z])',text):
                if len(sentence)<20:continue
                ids=[cid for cid,doc,meta in zip(corpus['ids'],corpus['documents'],corpus['metadatas']) if meta.get('page')==group['page'] and norm(sentence) in norm(doc)]
                groups.append({'page':group['page'],'quote':sentence,'alternatives':ids})
        mapping[row['id']]=groups
    return mapping


def retrieval_score(chunks,groups,k):
    if not groups:return None
    ids={c['chunk_id'] for c in chunks[:k]}
    return sum(bool(ids&set(g['alternatives'])) for g in groups)/len(groups)


def answer_score(text,row):
    spans=row['required_exact_spans']
    if not spans:return {'exact_span_coverage':None,'semantic_correctness':'pending_human_review'}
    hits=[s for s in spans if norm(s) in norm(text)]
    return {'required_spans':len(spans),'matched_spans':len(hits),'exact_span_coverage':len(hits)/len(spans),
            'missing_exact_spans':[s for s in spans if s not in hits],
            'semantic_correctness':'pending_human_review',
            'note':'Strict textual lower-bound coverage; faithful paraphrases may miss. Not an accuracy label.'}


def model_answer_for_scoring(record,raw_output):
    """Score the literal proposed selection before semantic review, not JSON IDs.

    Historical free-text records remain supported. Missing/invalid selections
    yield no answer text; raw generation is retained separately for inspection.
    """
    if 'proposed_answer' in record:
        return record['proposed_answer'] or ''
    return raw_output


def score_run(folder,labels_path):
    folder=Path(folder);rows=json.loads(Path(labels_path).read_text());byid={r['id']:r for r in rows};mapping=json.loads((folder/'evidence_mapping.json').read_text())
    records=[]
    for p in sorted(folder.glob('fresh-*.json')):
        d=json.loads(p.read_text());row=byid[d['question']['id']];t=d.get('trace',{});pre=d.get('retrieval_before_merge',[]);chunks=pre[0]['chunks'] if pre else []
        groups=mapping[row['id']]
        calls=d.get('provider_calls',[]);answers=[c for c in calls if c['messages'][0]['content'].startswith('You are a university policy assistant')]
        raw=answers[-1].get('response',{}).get('text','') if answers else ''
        raw_output=raw
        raw=model_answer_for_scoring(d,raw_output)
        raw_response=answers[-1].get('response',{}) if answers else {}
        hitids={cid for g in groups for cid in g['alternatives']}
        ranks=[i for i,c in enumerate(chunks,1) if c['chunk_id'] in hitids]
        providers=[c['response'] for c in calls if c.get('response')]
        records.append({'id':row['id'],'mode':d['mode'],'expected':row['expect'],'decision':t.get('decision','error'),'reason':t.get('abstain_reason') or d.get('error'),
            'hyde_fallback':t.get('hyde_failed',False),'unmapped_groups':sum(not g['alternatives'] for g in groups),
            'mapping_complete':all(g['alternatives'] for g in groups),
            'retrieval_scoring_status':'unscored_incomplete_mapping' if any(not g['alternatives'] for g in groups) else 'mapped' if groups else 'out_of_scope_no_relevance_target',
            'evidence_group_recall':{str(k):retrieval_score(chunks,groups,k) for k in (1,3,5)},
            'reciprocal_rank':(1/min(ranks) if ranks else 0) if groups and all(g['alternatives'] for g in groups) else None,
            'raw_answer':answer_score(raw,row),'final_answer':answer_score(t.get('answer',''),row),
            'raw_generated':bool(raw_output),'raw_finish_reason':raw_response.get('finish_reason'),
            'source_completion':any('appended verbatim' in w for w in t.get('warnings',[])),
            'final_citation_checks_passed':t.get('citations_verified',False),
            'raw_quote_verified':len(d.get('raw_quotation_attribution',{}).get('verified',[])),
            'raw_quote_failed':len(d.get('raw_quotation_attribution',{}).get('failed',[])),
            'raw_model_output':raw_output,'raw_model_answer':raw,'final_application_answer':t.get('answer',''),
            'latency_seconds':d.get('elapsed_s'),'stage_timings_ms':t.get('timings_ms',{}),
            'reported_successful_call_tokens':{k:sum(c.get(k) or 0 for c in providers) for k in ('input_tokens','output_tokens','reasoning_tokens')},
            'failed_attempt_tokens':'unknown; provider may not report failed-request usage',
            'abstention_human_grade':'pending','raw_semantic_grade':'pending','final_semantic_grade':'pending'})
    metrics={'review_type':'AI-reviewed labels, not human verified','observations':records,'accuracy':None,
             'note':'No semantic accuracy or superiority computed. Fallbacks are service observations, not genuine HyDE quality.'}
    aggregates={}
    for mode in ('raw','hyde','fusion'):
        rs=[r for r in records if r['mode']==mode]
        quality=[r for r in rs if r['expected']=='answer' and r['mapping_complete'] and not r['hyde_fallback'] and r['decision'] not in {'provider_unavailable','error'}]
        aggregates[mode]={'service_attempts':len(rs),'accepted':sum(r['decision']=='answered' for r in rs),
            'genuine_mapped_quality_cases':len(quality),
            'source_group_recall_at_k':{str(k):statistics.mean(r['evidence_group_recall'][str(k)] for r in quality) if quality else None for k in (1,3,5)},
            'mrr_first_relevant':statistics.mean(r['reciprocal_rank'] for r in quality) if quality else None,
            'semantic_accuracy':None}
    paired=[]
    for ident in sorted({r['id'] for r in records}):
        a=next((r for r in records if r['id']==ident and r['mode']=='raw'),None)
        b=next((r for r in records if r['id']==ident and r['mode']=='hyde'),None)
        if a and b and a['expected']=='answer' and a['mapping_complete'] and b['mapping_complete'] and not b['hyde_fallback'] and a['reciprocal_rank'] is not None and b['reciprocal_rank'] is not None:
            delta=b['reciprocal_rank']-a['reciprocal_rank']
            paired.append({'id':ident,'raw_rr':a['reciprocal_rank'],'hyde_rr':b['reciprocal_rank'],'outcome':'win' if delta>0 else 'loss' if delta<0 else 'tie'})
    metrics['paired_genuine_raw_hyde']={'pairs':paired,'n':len(paired),'wins':sum(r['outcome']=='win' for r in paired),'ties':sum(r['outcome']=='tie' for r in paired),'losses':sum(r['outcome']=='loss' for r in paired)}
    metrics['exploratory_retrieval_aggregates']=aggregates
    (folder/'metrics.json').write_text(json.dumps(metrics,indent=2))
    lines=['# Exploratory frozen-set execution results','', 'Labels: AI-assisted review, **not human verified**. No semantic accuracy claim. All ten questions were frozen before this run; after inspection they are no longer an untouched set for further tuning.','', '| Case | Mode | Decision/reason | Group recall@3 | Raw exact-span coverage | Final exact-span coverage | Fallback | Supplement |','|---|---|---|---|---|---|---|---|']
    for r in records:lines.append(f"| {r['id']} | {r['mode']} | {r['decision']}/{r['reason'] or '—'} | {r['evidence_group_recall']['3'] if r['mapping_complete'] else 'unscored: mapping incomplete'} | {r['raw_answer']['exact_span_coverage']} | {r['final_answer']['exact_span_coverage']} | {r['hyde_fallback']} | {r['source_completion']} |")
    lines+=['','Exploratory genuine-mode retrieval aggregates (AI-reviewed relevance only; excluded fallbacks/unmapped cases):','```json',json.dumps(aggregates,indent=2),'```','','Per-mode aggregates use different eligible subsets and must not be compared directly. Same-case genuine Raw/HyDE pairs:','```json',json.dumps(metrics['paired_genuine_raw_hyde'],indent=2),'```']
    lines+=['','Exact-span coverage is deliberately literal; it measures inclusion of rubric phrases, not whether paraphrases are correct or the answer is safe. Application acceptance is not human correctness. Complete evidence groups and alternatives are in evidence_mapping.json. No verified labels were written.','', '## Per-mode service observations']
    for mode in ('raw','hyde','fusion'):
        rs=[r for r in records if r['mode']==mode];lat=sorted(r['latency_seconds'] for r in rs if r['latency_seconds'] is not None)
        lines+=['',f"- {mode}: {len(rs)} recorded; accepted {sum(r['decision']=='answered' for r in rs)}; fallback {sum(r['hyde_fallback'] for r in rs)}; source-completed {sum(r['source_completion'] for r in rs)}; median request seconds {statistics.median(lat) if lat else None}; observed p95 seconds {lat[math.ceil(.95*len(lat))-1] if lat else None} (small sample)."]
    lines+=['','## Human grading still required','', 'Review every raw/final answer against the frozen rubric for correct meaning, all qualifications, no invented claims, appropriate abstention, and citations. Blind mode identity where feasible. No automatic checker substitutes for that judgment. Exclude provider/local quota failures from semantic abstention grading but report them in service coverage. Review errors and unmapped groups rather than silently dropping cases.','', '## Full outputs']
    for p in sorted(folder.glob('fresh-*.json')):
        d=json.loads(p.read_text());lines+=['',f"### {d['question']['id']} / {d['mode']}",'',d['question']['query'],'','Raw model answer:','```text']
        ans=[c for c in d['provider_calls'] if c['messages'][0]['content'].startswith('You are a university policy assistant')]
        lines += [(ans[-1].get('response',{}).get('text') or '[no usable model answer]') if ans else '[generation not called]','```','','Final application answer:','```text',d.get('trace',{}).get('answer') or '[none]','```','',f"Full source/prompt/score record: [{p.name}]({p.name})"]
    (folder/'RESULTS.md').write_text('\n'.join(lines));return metrics
