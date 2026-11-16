"""Read archived traces and replay context selection; no LLM, index or writes."""
import json
from src.evidence import normalize
from src.answer import answer_evidence
from src.store import RetrievedChunk


def contains(text,quote):return normalize(quote) in normalize(text or '')


def audit_record(record,targets):
    candidates=record.get('retrieval_before_merge',[{'chunks':[]}])[0]['chunks']
    blocks=record.get('trace',{}).get('retrieved',[])
    replay=[]
    for row in candidates:
        replay.append(RetrievedChunk(**{k:v for k,v in row.items() if k in RetrievedChunk.__dataclass_fields__}))
    selected=answer_evidence(record['question']['query'],replay)
    output=[]
    for target in targets:
        quote=target['quote']
        ranks=[i for i,c in enumerate(candidates,1) if contains(c['text'],quote)]
        sent=any(contains(c.get('answer_excerpt'),quote) for c in blocks)
        output.append({'page':target['page'],'quote':quote,'candidate_ranks':ranks,
                       'stored_retrieved_block':any(contains(c.get('text'),quote) for c in blocks),
                       'sent_in_archived_context':sent,
                       'in_archived_final_answer':contains(record['trace'].get('answer'),quote),
                       'in_current_selector_replay':any(contains(c.text,quote) for c in selected),
                       'loss_stage': 'context_selection' if ranks and not sent else 'not_in_candidates' if not ranks else 'after_context_or_none'})
    return output
