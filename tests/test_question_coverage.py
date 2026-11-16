"""Requirements are question spans; coverage is not inferred from keyword matches."""
import pytest
from src.question_coverage import question_requirements, coverage_failures


def rows(question, refs=None):
    return [{'requirement_id':r['id'],'status':'covered','evidence':refs or ['C1/P1'],'reason':''}
            for r in question_requirements(question)]


def test_compound_question_keeps_scope_and_each_explicit_part():
    q='Under the visiting-student scheme, what is the charge and when is the application due?'
    req=question_requirements(q)
    assert req[0]['text']==q
    assert len(req)==3
    assert 'when is the application due' in req[2]['text']
    assert all(q[r['start']:r['end']]==r['text'] for r in req)


def test_deadline_and_fee_are_both_visible_without_institution_vocabulary():
    q='Can passing every subject waive the registration deadline and fee?'
    assert question_requirements(q)[-1]['text']=='fee?'


@pytest.mark.parametrize('status',['unsupported','ambiguous'])
def test_aggregate_approval_cannot_hide_uncovered_part(status):
    q='What is the charge and when is the application due?'
    r=rows(q);r[-1].update(status=status,evidence=[],reason='No applicable passage')
    assert any(f['reason']=='coverage_'+status for f in coverage_failures(r,question_requirements(q),{'C1/P1'}))


def test_cannot_use_unselected_or_unknown_source_for_coverage():
    q='What is the charge?'
    assert coverage_failures(rows(q,['C2/P8']),question_requirements(q),{'C1/P1'})


def test_missing_and_duplicate_requirement_rows_fail_closed():
    q='What is the charge and when is it due?';r=rows(q)
    assert coverage_failures(r[:-1],question_requirements(q),{'C1/P1'})
    assert coverage_failures(r+[r[0]],question_requirements(q),{'C1/P1'})


def test_single_question_no_policy_specific_inferences():
    assert len(question_requirements('Who decides?'))==1
    assert coverage_failures([],question_requirements('Who decides?'),set())


def test_actual_summer_fee_and_deadline_survive_current_selector():
    from pathlib import Path
    from src.answer import answer_evidence
    from tests.test_guardrails import make_chunk
    c=make_chunk(text=(Path(__file__).parent/'fixtures/coverage/nit_goa_summer_actual.txt').read_text(),page=12)
    sent=answer_evidence('Will passing every summer subject let me ignore the summer registration deadline and fee?',[c])
    assert 'B17.2.' in sent[0].text and 'B17.5.' in sent[0].text
    assert '₹ 5000/- per course' in sent[0].text
    assert 'The amount will change periodically as per Senate approval.' in sent[0].text
    assert sent[0].page==12 and sent[0].chunk_id==c.chunk_id


def test_trace_audit_distinguishes_candidate_loss_from_context_loss():
    from evaluation.ps1.refinements.trace_failure import audit_record
    from dataclasses import asdict
    from tests.test_guardrails import make_chunk
    c=make_chunk(text='R1. Applications are due in six days. R2. The charge is 41 units.')
    record={'question':{'query':'What is the deadline and charge?'},'retrieval_before_merge':[{'chunks':[asdict(c)]}],
            'trace':{'retrieved':[{'text':c.text,'answer_excerpt':'R1. Applications are due in six days.'}],'answer':''}}
    result=audit_record(record,[{'page':3,'quote':'R2. The charge is 41 units.'}])[0]
    assert result['candidate_ranks']==[1] and result['loss_stage']=='context_selection'
    assert result['in_current_selector_replay']


@pytest.mark.asyncio
async def test_partial_coverage_rejected_even_with_all_four_aggregate_approvals(monkeypatch):
    import json
    from types import SimpleNamespace
    from unittest.mock import AsyncMock
    from src import answer
    from tests.test_guardrails import make_chunk
    from tests.grounding_helpers import selection,accepted_review
    q='What is the charge and when is it due?'
    c=make_chunk(text='R1. The charge is 41 credits.')
    review=json.loads(accepted_review(q));review['coverage'][-1].update(status='unsupported',evidence=[],reason='Deadline missing')
    monkeypatch.setattr('src.store.valid_cached_citations',lambda ids:True)
    chat=AsyncMock(side_effect=[SimpleNamespace(text=selection(c.text)),SimpleNamespace(text=json.dumps(review))])
    monkeypatch.setattr(answer,'get_llm_client',lambda:SimpleNamespace(chat=chat))
    text,reason,_,response=await answer.generate_answer(q,[c])
    assert reason=='question_coverage_failed' and text==answer.ABSTAIN_MESSAGE
    assert any(f['reason']=='coverage_unsupported' for f in response.validation_failures)


def test_legacy_boolean_only_review_is_not_a_new_cache_proof():
    from src.grounding import make_proof,proof_matches
    from tests.grounding_helpers import selection
    from tests.test_guardrails import make_chunk
    import json
    c=make_chunk(text='R1. The charge is 41 credits.')
    old={'relevant':True,'complete':True,'supported':True,'qualifications_preserved':True,'reasons':[]}
    proof=make_proof('What is the charge?','"'+c.text+'" [C1]',[c],json.loads(selection(c.text)),old)
    assert not proof_matches(proof,'What is the charge?','"'+c.text+'" [C1]',[c])


def test_exact_live_summer_review_missing_rows_remains_a_rejected_development_case():
    import json
    from pathlib import Path
    from src.grounding import review_passes
    review=json.loads((Path(__file__).parent/'fixtures/coverage/summer_review_missing_rows.json').read_text())
    q='Will passing every summer subject let me ignore the summer registration deadline and fee?'
    required=question_requirements(q)
    failures=coverage_failures(review['coverage'],required,{'C1/P1','C1/P2'})
    missing={r['requirement_id'] for r in failures if r['reason']=='coverage_requirement_missing'}
    assert missing=={'Q1','Q2'}
    assert not review_passes(review,required,{'C1/P1','C1/P2'})


@pytest.mark.parametrize('contract',[None,[],['status','claims'],'invalid'])
def test_malformed_cached_contract_cannot_crash_coverage_validation(contract):
    from src.question_coverage import selected_references
    assert selected_references(contract,[])==set()
