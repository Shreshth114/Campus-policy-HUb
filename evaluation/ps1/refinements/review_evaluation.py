"""Offline review scoring. Human decisions are inputs, never generated labels."""
import argparse
import json
import statistics
from pathlib import Path
from types import SimpleNamespace
from src.grounding import review_passes
from src.question_coverage import question_requirements,selected_references

DIMENSIONS=('relevant','complete','supported','qualifications_preserved')


def human_label_complete(row):
    return (row.get('source_pdf_checked') is True and row.get('human_reviewed') is True and row.get('review_origin')=='human'
            and isinstance(row.get('reviewer'),str) and bool(row['reviewer'].strip())
            and row.get('adjudication_status')=='final'
            and isinstance(row.get('dimensions'),dict)
            and all(type(row['dimensions'].get(k)) is bool for k in DIMENSIONS)
            and type(row.get('selection_acceptable')) is bool
            and type(row.get('citation_correct')) is bool
            and row.get('appropriate_outcome') in ('answer','withhold','clarify')
            and isinstance(row.get('notes'),str) and bool(row['notes'].strip())
            and isinstance(row.get('required_qualifications'),list)
            and isinstance(row.get('atomic_requirements'),list) and bool(row['atomic_requirements'])
            and isinstance(row.get('supporting_provisions'),list) and bool(row['supporting_provisions'])
            and (not row['selection_acceptable'] or (all(row['dimensions'][k] for k in DIMENSIONS)
                                                   and row['citation_correct'] and row['appropriate_outcome']=='answer')))


def unique(rows,key):
    mapped={r[key]:r for r in rows}
    if len(mapped)!=len(rows):raise ValueError('Duplicate '+key)
    return mapped


def score(cases,annotations,predictions):
    case_map=unique(cases,'id');humans=unique(annotations,'case_id');preds=unique(predictions,'case_id')
    if (set(humans)|set(preds))-set(case_map):raise ValueError('Unknown case ID')
    scored=[];usage=[];service_errors=0
    for cid,pred in preds.items():
        u=pred.get('usage')
        if isinstance(u,dict) and u:usage.append(u)
        if pred.get('error'):
            service_errors+=1
            continue
        human=humans.get(cid,{})
        if not human_label_complete(human):continue
        case=case_map[cid];verdict=pred.get('review')
        chunks=[SimpleNamespace(text=c['text']) for c in case['chunks']]
        selected=selected_references(case['selection'],chunks)
        approved=review_passes(verdict,question_requirements(case['question']),selected)
        raw_approval=isinstance(verdict,dict) and all(verdict.get(k) is True for k in DIMENSIONS)
        scored.append((human,verdict,approved,raw_approval))
    positives=sum(h['selection_acceptable'] for h,_,_,_ in scored)
    negatives=len(scored)-positives
    def rate(num,denom):return num/denom if denom else None
    latency=[u['latency_ms'] for u in usage if type(u.get('latency_ms')) in (int,float) and u['latency_ms']>=0]
    tokens={key:sum(u[key] for u in usage if type(u.get(key)) is int and u[key]>=0)
            for key in ('input_tokens','output_tokens','reasoning_tokens')}
    return {'service_error_cases':service_errors,'cases':len(cases),'prediction_cases':len(preds),'human_scored_cases':len(scored),
            'unscored_cases':len(cases)-len(scored),'evaluation_complete':len(scored)==len(cases) and bool(cases),
            'acceptable_denominator':positives,'unacceptable_denominator':negatives,
            'false_approval_rate':rate(sum(a and not h['selection_acceptable'] for h,_,a,_ in scored),negatives),
            'false_rejection_rate':rate(sum(not a and h['selection_acceptable'] for h,_,a,_ in scored),positives),
            'raw_boolean_false_approval_rate':rate(sum(a and not h['selection_acceptable'] for h,_,_,a in scored),negatives),
            'dimension_accuracy':{k:rate(sum(isinstance(v,dict) and type(v.get(k)) is bool and v[k]==h['dimensions'][k] for h,v,_,_ in scored),len(scored)) for k in DIMENSIONS},
            'review_observations':len(usage),'latency_observations':len(latency),
            'review_median_provider_latency_ms':statistics.median(latency) if latency else None,
            'reported_review_tokens':tokens,
            'token_observations':{key:sum(type(u.get(key)) is int and u[key]>=0 for u in usage) for key in tokens},
            'note':'Pending humans are unscored. Provider errors need separate service reporting. Reasoning tokens are part of output tokens, not an additional billable sum. Provider latency excludes unreported queue/wait time; no currency prices assumed.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--cases',required=True);parser.add_argument('--annotations',required=True)
    parser.add_argument('--predictions',required=True);parser.add_argument('--output',required=True);args=parser.parse_args()
    result=score(*[json.loads(Path(p).read_text()) for p in (args.cases,args.annotations,args.predictions)])
    with Path(args.output).open('x') as stream:
        stream.write('# Coverage-review evaluation\n\n```json\n'+json.dumps(result,indent=2)+'\n```\n')

if __name__=='__main__':main()
