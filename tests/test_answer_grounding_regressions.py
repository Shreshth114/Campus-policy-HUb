"""No live model, embeddings or databases: regressions for answer grounding."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from src import answer, evidence, pipeline
from tests.grounding_helpers import selection,accepted_review
from src.trace import ChunkTrace
from src.retrieve import RetrievalResult
from tests.test_guardrails import make_chunk

QUESTION = 'What attendance is required for medical condonation and minimum overall attendance?'
PAGE = (Path(__file__).parent/'fixtures/chunking/nit_goa_page_10.txt').read_text()
PROVISION = ' '.join(PAGE[PAGE.index('B11.4.'):PAGE.index('B11.5.')].split())
THRESHOLDS = 'Medical condonation requires at least 80% attendance excluding medical leave and at least 75% overall attendance including medical leave [C1].'
CONDITIONS = ('Application for condonation, recommended by the Faculty Advisor, concerned faculty and the HoD is to be submitted to the AAC on or before the last instructional day of the semester [C1]. '
 'The AAC, depending on the merit of the case may permit the student to appear for the end semester exam [C1]. '
 'A student will be eligible for this concession at most in two semesters during the entire degree programme [C1]. '
 'Application for medical leave, supported by medical certificate with endorsement by the Institute Medical Officer (IMO), should reach the HoD within seven days after returning from leave or, on or before the last instructional day of the semester, whichever is earlier [C1].')
CORRECT = THRESHOLDS+'\n'+CONDITIONS


def attendance():
    return make_chunk(text=PAGE, similarity=.95)


def test_complete_b114_reaches_prompt_with_citation_mapping():
    text=answer._extract_prompt_text(answer._build_answer_prompt(QUESTION,[attendance()]))
    from html import unescape
    assert PROVISION in ' '.join(unescape(text).split())
    assert '<excerpt id="C1"' in text
    assert 'p.3' in text


@pytest.mark.parametrize('response,accept',[
 (CORRECT,True),
 (THRESHOLDS,False),
 (CORRECT.replace('The AAC, depending on the merit of the case may permit the student to appear for the end semester exam [C1]. ', ''),False),
 (CORRECT.replace('80%', '60%'),False),
 (CORRECT.replace('80%', 'XX%').replace('75%','80%').replace('XX%','75%'),False),
 (CORRECT+'\nAttendance below 75% requires repeating coursework [C1].',False),
 (CORRECT+'\nThe absolute minimum is 60%.',False),
])
@pytest.mark.asyncio
async def test_generation_grounding(monkeypatch,response,accept):
    monkeypatch.setattr('src.store.valid_cached_citations',lambda ids:True)
    # Keep the original paraphrase validator regression in addition to the
    # new generation contract. Production renders only complete exact units.
    source=attendance();source.text=PROVISION
    assert (answer.validate_answer(response,[source])[0] is None)==accept
    if accept:
        model_response=selection(PROVISION)
    else:
        model_response=selection(response)
    chat=AsyncMock(side_effect=[SimpleNamespace(text=model_response),SimpleNamespace(text=accepted_review(QUESTION,['C1/P5']))])
    monkeypatch.setattr(answer,'get_llm_client',lambda:SimpleNamespace(chat=chat))
    result,reason,_,_=await answer.generate_answer(QUESTION,[attendance()])
    assert (reason is None)==accept
    if not accept:assert result==answer.ABSTAIN_MESSAGE


@pytest.mark.asyncio
async def test_cache_does_not_bypass_uncited_claim_validation(monkeypatch):
    c=attendance()
    cached={'answer':'The absolute minimum is 60%.\nAttendance is covered [C1].','citations':[c.chunk_id],
            'retrieved':[dict(chunk_id=c.chunk_id,doc_id=c.doc_id,doc_title=c.doc_title,section=c.section,page=c.page,score=.95,text_preview='',text=c.text,institution_id=c.institution_id)]}
    monkeypatch.setattr(pipeline,'cache_lookup',lambda q:cached)
    monkeypatch.setattr(pipeline,'valid_cached_citations',lambda ids:True)
    retrieve=AsyncMock(return_value=RetrievalResult(chunks=[],mode='fusion'))
    monkeypatch.setattr(pipeline,'retrieve',retrieve)
    trace=await pipeline.ask(QUESTION,'fusion')
    assert not trace.cache_hit
    assert trace.decision=='abstained'
    retrieve.assert_awaited_once()


@pytest.mark.asyncio
async def test_exact_sent_excerpt_not_hidden_full_chunk(monkeypatch):
    c=make_chunk(text=PROVISION+'\nB12. Other Rule\nThe fee is 999 units.')
    monkeypatch.setattr('src.store.valid_cached_citations',lambda ids:True)
    monkeypatch.setattr(answer,'get_llm_client',lambda:SimpleNamespace(chat=AsyncMock(return_value=SimpleNamespace(text='The fee is 999 units [C1].'))))
    _,reason,_,_=await answer.generate_answer(QUESTION,[c])
    assert reason is not None


def test_foreign_workspace_cannot_enter_answer():
    c=attendance();c.workspace_id='foreign-workspace';c.institution_id=''
    assert answer.confidence_gate([c])==(False,'foreign_evidence')


def test_hyde_cannot_enter_prompt():
    c=attendance()
    result=RetrievalResult(chunks=[c],mode='fusion',hyde_text='HYDE_POISON_60_PERCENT')
    assert 'HYDE_POISON' not in answer._extract_prompt_text(answer._build_answer_prompt(QUESTION,result.chunks))


@pytest.mark.asyncio
async def test_oversized_provision_abstains_without_model(monkeypatch):
    c=make_chunk(text='B11.4. '+('An indivisible provision has a long condition. '*200))
    client=AsyncMock()
    monkeypatch.setattr(answer,'get_llm_client',client)
    monkeypatch.setattr('src.store.valid_cached_citations',lambda ids:True)
    assert (await answer.generate_answer('condition?', [c]))[1]=='incomplete_evidence_context'
    client.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize('cached_answer',[CORRECT, CORRECT.replace('80%', '60%'),THRESHOLDS,CORRECT+'\nRepeat coursework [C1].'])
async def test_cache_exact_excerpts_revalidated(monkeypatch,cached_answer):
    c=attendance()
    cached={'answer':cached_answer,'citations':[c.chunk_id], 'retrieved':[
        dict(chunk_id=c.chunk_id,doc_id=c.doc_id,doc_title=c.doc_title,section=c.section,page=c.page,
             score=.95,text_preview='',text=c.text,answer_excerpt=answer.trim_chunk_span(c.text,QUESTION),institution_id=c.institution_id)]}
    monkeypatch.setattr(pipeline,'cache_lookup',lambda q:cached)
    monkeypatch.setattr(pipeline,'valid_cached_citations',lambda ids:True)
    monkeypatch.setattr(pipeline,'retrieve',AsyncMock(return_value=RetrievalResult(chunks=[],mode='fusion')))
    result=await pipeline.ask(QUESTION,'fusion')
    assert not result.cache_hit  # Legacy entries lack a question-coverage review proof.


def test_diagnostics_opt_in_and_secret_redaction(tmp_path,monkeypatch):
    import json
    from src.answer_diagnostics import record_answer
    from src.config import PROVIDERS
    c=attendance();sent=answer.answer_evidence(QUESTION,[c]);folder=tmp_path/'logs'
    monkeypatch.setenv('ANSWER_DIAGNOSTICS_DIR',str(folder))
    monkeypatch.delenv('ANSWER_DIAGNOSTICS_ENABLED',raising=False)
    record_answer([], [c],sent,'bad','unsupported',[])
    assert not folder.exists()
    monkeypatch.setenv('ANSWER_DIAGNOSTICS_ENABLED','true')
    fake='gsk_FAKE_SECRET_DO_NOT_LOG'
    monkeypatch.setitem(PROVIDERS['groq'],'api_key',fake)
    messages=[{'role':'user','content':fake+' '+('A'*43)+' password=private123'}]
    record_answer(messages,[c],sent,fake,'unsupported',[{'reason':'uncited_claim'}])
    files=list(folder.glob('*.json'));assert len(files)==1
    raw=files[0].read_text();assert fake not in raw and 'A'*43 not in raw and 'private123' not in raw
    data=json.loads(raw);assert data['excerpts'][0]['label']=='C1'
    assert data['excerpts'][0]['page']==c.page
    assert data['excerpts'][0]['text']==sent[0].text
    assert data['failures'][0]['reason']=='uncited_claim'
    assert files[0].stat().st_mode & 0o777 == 0o600


def test_diagnostics_io_failure_does_not_change_outcome(tmp_path,monkeypatch):
    from src.answer_diagnostics import record_answer
    occupied=tmp_path/'file';occupied.write_text('occupied')
    monkeypatch.setenv('ANSWER_DIAGNOSTICS_ENABLED','true')
    monkeypatch.setenv('ANSWER_DIAGNOSTICS_DIR',str(occupied))
    c=attendance();record_answer([], [c],[c],'bad','rejected',[])


@pytest.mark.parametrize('claim',[
    'The AAC must permit the student to appear for the end semester exam [C1].',
    'Students are eligible without medical leave approval [C1].',
])
def test_invented_permission_is_rejected(claim):
    assert evidence.claim_failures(claim,[attendance()])


def test_exact_complete_provision_quotation_is_supported():
    c=attendance();c.text=PROVISION
    assert answer.validate_answer('"'+PROVISION+'" [C1].',[c])[0] is None


def test_ambiguous_multivalue_paraphrase_fails_closed():
    c=make_chunk(text='Minimum laboratory attendance is 80% with overall attendance 75%.')
    assert evidence.claim_failures('Minimum laboratory attendance is 75% with overall attendance 80% [C1].',[c])


def test_diagnostics_refuses_production_destination(monkeypatch):
    from src.answer_diagnostics import record_answer
    from src.config import PROJECT_ROOT
    monkeypatch.setenv('ANSWER_DIAGNOSTICS_ENABLED','true')
    monkeypatch.setenv('ANSWER_DIAGNOSTICS_DIR',str(PROJECT_ROOT/'data'/'forbidden-diagnostics'))
    c=attendance();record_answer([], [c],[c],'bad','rejected',[])
    assert not (PROJECT_ROOT/'data'/'forbidden-diagnostics').exists()
