"""General grounding mechanisms; synthetic policy text is never production data."""
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from src import answer
from tests.test_guardrails import make_chunk
from tests.test_answer_grounding_regressions import PROVISION, QUESTION


def payload(quote, source='C1'):
    return json.dumps({'status':'answer','claims':[{'quote':quote,'source':source}]})


def review(accepted=True,question='q'):
    from tests.grounding_helpers import accepted_review
    data=json.loads(accepted_review(question))
    if not accepted:
        for key in ('relevant','complete','qualifications_preserved','supported'):data[key]=False
        data['reasons']=['wrong situation']
        for row in data['coverage']:row.update(status='unsupported',evidence=[],reason='wrong situation')
    return json.dumps(data)


def test_complete_provision_and_second_rule_fit_existing_total_budget():
    c=make_chunk(text=PROVISION+'\nB12.1. A late request requires a processing fee of 43 credits.')
    sent=answer.answer_evidence(QUESTION+' What fee applies to a late request?', [c])
    assert PROVISION in sent[0].text
    assert '43 credits' in sent[0].text
    assert sum(len(x.text) for x in sent)<=4200


@pytest.mark.asyncio
@pytest.mark.parametrize('quote,ok',[
    ('R7. Students may borrow three books. Approval by the librarian is required within five days.',True),
    ('Students may borrow three books.',False),
    ('Students may borrow four books.',False),
    ('Students may borrow three',False),
])
async def test_other_institution_complete_rules_not_just_threshold(monkeypatch,quote,ok):
    c=make_chunk(text='R7. Students may borrow three books. Approval by the librarian is required within five days.')
    monkeypatch.setattr('src.store.valid_cached_citations',lambda ids:True)
    chat=AsyncMock(side_effect=[SimpleNamespace(text=payload(quote)),SimpleNamespace(text=review(question='How many books can I borrow and what approval is needed?'))])
    monkeypatch.setattr(answer,'get_llm_client',lambda:SimpleNamespace(chat=chat))
    result,reason,_,_=await answer.generate_answer('How many books can I borrow and what approval is needed?', [c])
    assert (reason is None)==ok
    assert chat.await_count==(2 if ok else 1)
    if not ok: assert result==answer.ABSTAIN_MESSAGE


@pytest.mark.asyncio
async def test_question_coverage_rejection_no_automatic_source_append(monkeypatch):
    c=make_chunk(text='A1. General registration is required every semester.')
    monkeypatch.setattr('src.store.valid_cached_citations',lambda ids:True)
    chat=AsyncMock(side_effect=[SimpleNamespace(text=payload(c.text)),SimpleNamespace(text=review(False))])
    monkeypatch.setattr(answer,'get_llm_client',lambda:SimpleNamespace(chat=chat))
    result,reason,_,response=await answer.generate_answer('How do I return after a temporary withdrawal?', [c])
    assert reason=='question_coverage_failed' and result==answer.ABSTAIN_MESSAGE
    assert response.validation_failures[0]['reason']=='question_coverage_failed'


def test_review_proof_bound_to_question_answer_evidence_and_scope():
    from src.grounding import make_proof, proof_matches
    c=make_chunk(text='R1. Students may borrow three books.')
    a='"'+c.text+'" [C1]'
    proof=make_proof('books?',a,[c],json.loads(payload(c.text)),json.loads(review()))
    assert proof_matches(proof,'books?',a,[c])
    assert not proof_matches(proof,'fees?',a,[c])
    assert not proof_matches(proof,'books?',a+' extra',[c])
    c.workspace_id='another'
    assert not proof_matches(proof,'books?',a,[c])


def test_same_line_individual_exact_quotes_do_not_form_false_combined_claim():
    c=make_chunk(text='Calculators are prohibited. The Senate may grant an exception.')
    assert answer.validate_answer('"Calculators are prohibited." [C1] "The Senate may grant an exception." [C1]',[c])[0] is None

@pytest.mark.parametrize('mutate',[
    lambda r:r.update(complete=False),
    lambda r:r.update(qualifications_preserved=False),
    lambda r:r.update(supported=False),
    lambda r:r.update(relevant='true'),
    lambda r:r.update(reasons=['unresolved exception']),
    lambda r:r.update(extra='unexpected'),
])
def test_review_is_fail_closed(mutate):
    from src.grounding import review_passes
    data=json.loads(review());mutate(data)
    assert not review_passes(data)


def test_later_retrieved_rule_can_supply_second_requested_part():
    chunks=[make_chunk(str(i),text='Unrelated cafeteria opening hours are fixed.') for i in range(3)]
    chunks.append(make_chunk('fee',text='F9. A late registration fee is 43 credits.'))
    assert any('43 credits' in c.text for c in answer.answer_evidence('What is the late registration fee?',chunks))


@pytest.mark.asyncio
@pytest.mark.parametrize('verdict',[review(False),'not JSON',review().replace('true','false',1)])
async def test_semantic_review_never_overrides_deterministic_validation(monkeypatch,verdict):
    c=make_chunk(text='L1. The minimum laboratory attendance is 83 percent.')
    monkeypatch.setattr('src.store.valid_cached_citations',lambda ids:True)
    chat=AsyncMock(side_effect=[SimpleNamespace(text=payload(c.text)),SimpleNamespace(text=verdict)])
    monkeypatch.setattr(answer,'get_llm_client',lambda:SimpleNamespace(chat=chat))
    assert (await answer.generate_answer('What laboratory attendance is needed?', [c]))[1]=='question_coverage_failed'


def test_cross_page_continuation_preserves_source_mapping():
    from src.evidence import connect_continuations
    a=make_chunk('first',text='Q4. Permission may be considered for',page=4)
    b=make_chunk('second',text='students who apply within three days. Q5. A separate review is required.',page=5)
    a.version_id=b.version_id='same-version';a.chunk_index=8;b.chunk_index=9
    connected=connect_continuations([b,a])
    assert len(connected)==1
    assert connected[0].pages==[4,5] and connected[0].source_chunk_ids==['first','second']
    assert 'considered for students' in connected[0].text
    b.workspace_id='foreign'
    assert len(connect_continuations([a,b]))==2


def test_repetition_within_provision_is_not_removed():
    from src.grounding import provisions
    text='R1. Permission is required. Permission is required. Apply by Friday.'
    assert provisions(text)==[text]


def test_explicit_provision_selection_renders_all_conditions_without_repair():
    from src.grounding import render_contract
    c=make_chunk(text='L1. Books may be borrowed. Approval is required.\nL2. A late fee is 19 units.')
    rendered,failures=render_contract({'status':'answer','claims':[{'source':'C1','provision':'P1'}]},[c])
    assert not failures and rendered=='"L1. Books may be borrowed. Approval is required." [C1]'
    assert '19 units' not in rendered


@pytest.mark.parametrize('source,unit',[('C9','P1'),('C1','P0'),('C1','P9'),('C1','L1'),('C0','P1')])
def test_selection_never_guesses_source_or_provision(source,unit):
    from src.grounding import render_contract
    c=make_chunk(text='L1. Books may be borrowed. Approval is required.')
    assert render_contract({'status':'answer','claims':[{'source':source,'provision':unit}]},[c])[1]


def test_semantically_related_provision_not_dropped_for_zero_keyword_overlap():
    c=make_chunk(text='R1. A temporary withdrawal is permitted for one semester.\nR2. On resumption, the adviser determines the creditable courses with the departmental head.')
    sent=answer.answer_evidence('How do I return after a temporary withdrawal?', [c])
    assert 'R2.' in sent[0].text


def test_complete_rule_with_trailing_parenthetical_is_preserved():
    from src.grounding import provisions
    text='F4. The fee is 43 credits. The council may revise it. (Amended at the fifth meeting)'
    assert provisions(text)==[text]
