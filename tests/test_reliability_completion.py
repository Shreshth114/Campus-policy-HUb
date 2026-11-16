from types import SimpleNamespace
from src import answer,evidence
from tests.test_guardrails import make_chunk
from tests.test_answer_grounding_regressions import PROVISION,CORRECT


def test_deadline_paraphrase_supported_without_dropping_qualifications():
    assert not evidence.claim_failures(CORRECT.replace('on or before','no later than'),[SimpleNamespace(text=PROVISION)])


def test_generation_budget_covers_complete_source_with_reasoning_reserve():
    assert answer.generation_budget([SimpleNamespace(text=PROVISION)]) > 350
    assert answer.generation_budget([SimpleNamespace(text='short')]) == 350
    assert answer.generation_budget([SimpleNamespace(text='x'*10000)]) <= 1200


def test_diagnostics_keep_individual_failures():
    _,_,failures=answer.validate_answer('A minimum of 60 percent [C1].',[make_chunk()])
    assert any(f['reason']=='unsupported_claim_or_condition' for f in failures)


def test_changed_threshold_still_rejected_with_deadline_alias():
    assert evidence.claim_failures(CORRECT.replace('on or before','no later than').replace('80%','60%'),[SimpleNamespace(text=PROVISION)])


import pytest
@pytest.mark.asyncio
async def test_request_scoped_hyde_single_generation(monkeypatch):
    import asyncio
    from unittest.mock import AsyncMock
    from src import hyde
    fake=AsyncMock(return_value=('source search wording',None))
    monkeypatch.setattr(hyde,'_generate_hyde',fake)
    token=hyde.request_generations.set({})
    try:
        await asyncio.gather(hyde.generate_hyde('same question'),hyde.generate_hyde('same question'))
        assert fake.await_count==1
    finally:hyde.request_generations.reset(token)
    await hyde.generate_hyde('same question')
    assert fake.await_count==2


def test_only_missing_conditions_can_be_completed_from_exact_sources():
    c=make_chunk(text=PROVISION)
    initial='"'+PROVISION.split('Application for condonation')[0].strip()+'" [C1].'
    initial=initial.replace(chr(34),'“',1)
    end=initial.rfind(chr(34));initial=initial[:end]+'”'+initial[end+1:]
    initial=initial.replace(' [C1]','\u202f[C1]')
    completed,changed=answer.complete_source_conditions(initial,[c])
    assert changed and 'depending on the merit' in completed and 'Institute Medical Officer' in completed
    assert answer.validate_answer(completed,[c])[0] is None
    wrong='Attendance must be 60 percent [C1].'
    assert answer.complete_source_conditions(wrong,[c])==(wrong,False)


def test_skipped_heading_does_not_leave_an_empty_prompt_label():
    empty=make_chunk('heading',text='B11. Attendance')
    real=make_chunk('real',text='B11.4. '+PROVISION.split(' ',1)[1])
    sent=answer.answer_evidence('medical condonation?', [empty,real])
    assert [c.chunk_id for c in sent]==['real']
    prompt=answer._build_answer_prompt('medical condonation?',[empty,real])[1]['content']
    assert '<excerpt id="C1"' in prompt and '<excerpt id="C2"' not in prompt
