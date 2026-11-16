from evaluation.ps1.review_metrics import retrieval_score,answer_score,evidence_map


def test_alternatives_are_not_independent_requirements():
    groups=[{'alternatives':['a','b']},{'alternatives':['c']}]
    assert retrieval_score([{'chunk_id':'b'}],groups,3)==.5
    assert retrieval_score([{'chunk_id':'b'},{'chunk_id':'c'}],groups,3)==1
    assert retrieval_score([],[],3) is None


def test_no_manufactured_correctness_for_matching_words():
    r=answer_score('The rule is 80%.',{'required_exact_spans':['80%','approval']})
    assert r['exact_span_coverage']==.5 and r['semantic_correctness']=='pending_human_review'


def test_unmapped_requirement_not_dropped():
    groups=[{'alternatives':[]},{'alternatives':['a']}]
    assert retrieval_score([{'chunk_id':'a'}],groups,3)==.5


import pytest
@pytest.mark.asyncio
async def test_benchmark_clarification_is_not_scored_as_answer(monkeypatch):
    from bench import run_benchmark as bench
    from src.trace import Trace
    from unittest.mock import AsyncMock
    from tests.test_benchmark import query
    monkeypatch.setattr(bench,'ask',AsyncMock(return_value=Trace(question='q',mode='raw',decision='clarification_required')))
    result=await bench.evaluate_safety([query(verified=True)],'raw')
    assert result['clarification_requests']==1
    assert result['total_answered']==0 and result['citation_validity_rate'] is None


def test_structured_selection_scored_before_review_not_as_json_or_final_answer():
    from evaluation.ps1.review_metrics import model_answer_for_scoring
    raw='{"status":"answer","claims":[{"source":"C1","provision":"P2"}]}'
    record={'proposed_answer':'"A fee of 43 credits is required." [C1]','trace':{'answer':'abstained'}}
    assert model_answer_for_scoring(record,raw)==record['proposed_answer']
    assert model_answer_for_scoring({'proposed_answer':None},raw)==''
    assert model_answer_for_scoring({},'historical free text')=='historical free text'
