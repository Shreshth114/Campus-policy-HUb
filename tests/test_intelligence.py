"""Quote-bound extraction and deterministic comparisons; synthetic evidence only."""
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from src import intelligence as intel,personal,institutions
from src.llm import LLMResponse
from tests.test_personal import client,create,uploaded

QUOTE='SYNTHETIC TEST FIXTURE. Minimum attendance is at least 75 percent.'

def raw(**changes):
    return {'subject':'attendance','operator':'>=','value':75,'unit':'percent','verbatim_quote':QUOTE,'exceptions':[],**changes}

def chunk(**changes):
    return {'chunk_id':'c','text':QUOTE,'doc_title':'SYNTHETIC TEST FIXTURE','doc_id':'d','version_id':'v','page':1,**changes}

@pytest.mark.parametrize('changes',[{'verbatim_quote':'fabricated quote 75'},{'value':90},{'operator':'<='},{'value':'NaN'},{'exceptions':['invented permission']},{'applies_to':'all colleges'}])
def test_unverifiable_rules_rejected(changes):assert intel.validate_rule(raw(**changes),chunk()) is None

@pytest.mark.parametrize('value,status,verdict',[(78,'satisfied','eligible'),(74,'not satisfied','ineligible')])
def test_code_decides(value,status,verdict):
    rule=intel.validate_rule(raw(),chunk())
    result=intel.evaluate([rule],[{'subject':'attendance','value':str(value),'unit':'%'}],True)
    assert result['conditions'][0]['status']==status and result['verdict']==verdict


def test_missing_ambiguous_units_applicability_and_no_rules_abstain():
    rule=intel.validate_rule(raw(),chunk())
    assert intel.evaluate([rule],[],True)['missing_facts']==['attendance']
    assert intel.evaluate([rule],[{'subject':'attendance','value':'78','unit':'marks'}],True)['verdict']=='insufficient evidence'
    assert intel.evaluate([rule],[{'subject':'attendance','value':'78','unit':'%'}],False)['verdict']=='insufficient evidence'
    assert intel.evaluate([],[],True)['abstained']


def test_rules_extraction_caches_only_verified_quotes(client,monkeypatch):
    wid,headers=create(client);entry=uploaded(client,headers,QUOTE)
    detail=client.get('/personal/documents/'+entry['doc_id'],headers=headers).json();cid=detail['chunks'][0]['chunk_id']
    responses=AsyncMock(return_value=LLMResponse(json.dumps({'rules':[raw(chunk_id=cid),raw(chunk_id=cid,value=99)]}),'fixture','fixture',1))
    monkeypatch.setattr(intel,'get_llm_client',lambda:SimpleNamespace(chat=responses))
    response=client.post('/personal/rules/extract',headers=headers,json={}).json()
    assert response['rules']==1 and response['discarded']==1
    assert client.post('/personal/rules/extract',headers=headers,json={}).json()['cached_documents']==1
    assert responses.await_count==1
    rules=client.get('/personal/rules',headers=headers).json()['rules'];assert rules[0]['page']==1 and rules[0]['workspace_id']==wid
    other,foreign=create(client);assert client.get('/personal/rules',headers=foreign).json()['rules']==[]
    monkeypatch.setattr(intel,'get_llm_client',lambda:SimpleNamespace(chat=AsyncMock(return_value=LLMResponse(json.dumps({'facts':[{'subject':'attendance','value':78,'unit':'percent','quote':'78% attendance'},{'subject':'attendance','value':99,'unit':'percent','quote':'78% attendance'}]}),'fixture','fixture',1))))
    facts=client.post('/personal/facts/parse',headers=headers,json={'text':'I have 78% attendance'}).json()
    assert len(facts['facts'])==1 and facts['confirmation_required']
    body={'question':'What attendance requirement applies?','facts':[{'subject':'attendance','value':'78','unit':'%'}],'confirmed':False}
    assert client.post('/personal/analyse',headers=headers,json=body).status_code==422
    body.update(confirmed=True,applicability_confirmed=True)
    # A fabricated model verdict cannot alter code's result.
    monkeypatch.setattr(intel,'get_llm_client',lambda:SimpleNamespace(chat=AsyncMock(return_value=LLMResponse('{"verdict":"ineligible","explanations":[]}','fixture','fixture',1))))
    analysis=client.post('/personal/analyse',headers=headers,json=body).json()
    assert analysis['verdict']=='eligible' and analysis['conditions'][0]['status']=='satisfied'
    client.delete('/personal/documents/'+entry['doc_id'],headers=headers)
    assert not client.get('/personal/rules',headers=headers).json()['rules']


def test_possible_conflicts_show_both_sources_and_do_not_choose_a_winner():
    left=intel.validate_rule(raw(),chunk())
    right=intel.validate_rule(raw(value=80,verbatim_quote=QUOTE.replace('75','80')),chunk(text=QUOTE.replace('75','80'),doc_id='other',doc_title='SYNTHETIC TEST FIXTURE NEW',chunk_id='other'))
    conflicts=intel.conflicts_from_rules([left,right])
    assert len(conflicts)==1 and conflicts[0]['winner'] is None
    assert len(conflicts[0]['evidence'])==2 and all(r['page']==1 for r in conflicts[0]['evidence'])
    result=intel.evaluate([left,right],[{'subject':'attendance','value':'78','unit':'%'}],True,conflicted={'attendance'})
    assert result['verdict']=='insufficient evidence'
    assert all(c['status']=='insufficient evidence' for c in result['conditions'])
    assert intel.conflicts_from_rules([left,{**left,'rule_id':'same','document_id':'other'}])==[]


def test_version_diff_preserves_both_quotes_and_does_not_assert_authority():
    old=intel.validate_rule(raw(),chunk())
    new=intel.validate_rule(raw(value=80,verbatim_quote=QUOTE.replace('75','80')),chunk(text=QUOTE.replace('75','80'),version_id='new'))
    result=intel.diff_rules([old],[new]);assert result[0]['kind']=='modification'
    assert result[0]['old'][0]['value']=='75' and result[0]['new'][0]['value']=='80'
    assert intel.diff_rules([],[new])[0]['kind']=='addition'
    assert intel.diff_rules([old],[])[0]['kind']=='removal'


def test_old_version_rules_remain_comparable_but_not_retrievable(client,monkeypatch):
    wid,headers=create(client);entry=uploaded(client,headers,QUOTE)
    def extraction_response(messages,**kwargs):
        rows=json.loads(messages[1]['content']);c=rows[0];value=80 if '80 percent' in c['text'] else 75
        return LLMResponse(json.dumps({'rules':[raw(chunk_id=c['chunk_id'],value=value,verbatim_quote=QUOTE.replace('75',str(value)))]}),'fixture','fixture',1)
    monkeypatch.setattr(intel,'get_llm_client',lambda:SimpleNamespace(chat=AsyncMock(side_effect=extraction_response)))
    assert client.post('/personal/rules/extract',headers=headers,json={}).json()['rules']==1
    from tests.test_personal import pdf
    newer=client.post('/personal/documents',headers=headers,data={'document_id':entry['doc_id']},files={'files':('SYNTHETIC NEW.pdf',pdf(QUOTE.replace('75','80')),'application/pdf')}).json()['documents'][0]['source']
    assert client.post('/personal/documents/'+entry['doc_id']+'/index',headers=headers,json={}).json()['status']=='ok'
    assert client.post('/personal/rules/extract',headers=headers,json={}).json()['rules']==1
    result=client.post('/personal/changes',headers=headers,json={'old_document_id':entry['doc_id'],'old_version_id':entry['version_id'],'new_document_id':newer['doc_id'],'new_version_id':newer['version_id']}).json()
    assert result['status']=='completed' and result['changes'][0]['kind']=='modification'
    assert all(r['value']=='80' for r in client.get('/personal/rules',headers=headers).json()['rules'])
    assert len(client.get('/personal/versions',headers=headers).json()['versions'])==2


@pytest.mark.parametrize('changes',[{'unit':'marks'},{'subject':'age'},{'verbatim_quote':QUOTE+' Unless prior approval is granted.'}])
def test_invented_units_subjects_and_omitted_exceptions_rejected(changes):
    source=chunk(text=QUOTE+' Unless prior approval is granted.')
    assert intel.validate_rule(raw(**changes),source) is None


def test_extraction_provider_failure_stays_partial_and_blocks_comparison(client,monkeypatch):
    from src.llm import ProviderUnavailableError
    _,headers=create(client);entry=uploaded(client,headers,QUOTE)
    monkeypatch.setattr(intel,'get_llm_client',lambda:SimpleNamespace(chat=AsyncMock(side_effect=ProviderUnavailableError('fixture',provider='groq',retry_after=500))))
    monkeypatch.setattr(intel.asyncio,'sleep',AsyncMock())
    result=client.post('/personal/rules/extract',headers=headers,json={'document_id':entry['doc_id']}).json()
    assert result['errors'] and result['status']=='partial'
    response=client.post('/personal/changes',headers=headers,json={'old_document_id':entry['doc_id'],'old_version_id':entry['version_id'],'new_document_id':entry['doc_id'],'new_version_id':entry['version_id']}).json()
    assert response['status']=='blocked'


def test_extraction_resume_skips_only_successful_batches(client,monkeypatch):
    from src.llm import ProviderUnavailableError
    from src.institutions import current
    _,headers=create(client);entry=uploaded(client,headers,QUOTE)
    rows=[chunk(chunk_id=f'chunk{i}',doc_id=entry['doc_id'],version_id=entry['version_id']) for i in range(7)]
    monkeypatch.setattr(intel,'chunks_for',lambda entry:rows)
    monkeypatch.setattr(intel,'RULE_EXTRACTION_PAUSE',0)
    seen=[];fail=True
    async def chat(messages,**kwargs):
        nonlocal fail
        batch=json.loads(messages[1]['content']);seen.append([c['chunk_id'] for c in batch])
        if fail and len(seen)==2:raise ProviderUnavailableError('fixture',provider='groq')
        return LLMResponse(json.dumps({'rules':[raw(chunk_id=batch[0]['chunk_id'])]}),'fixture','fixture',1)
    monkeypatch.setattr(intel,'get_llm_client',lambda:SimpleNamespace(chat=chat))
    first=client.post('/personal/rules/extract',headers=headers,json={'document_id':entry['doc_id']}).json()
    assert first['status']=='partial' and first['rules']==1
    fail=False;seen.clear()
    second=client.post('/personal/rules/extract',headers=headers,json={'document_id':entry['doc_id']}).json()
    assert second['status']=='complete' and second['rules']==3
    assert seen==[['chunk3','chunk4','chunk5'],['chunk6']]
    seen.clear()
    assert client.post('/personal/rules/extract',headers=headers,json={'document_id':entry['doc_id']}).json()['cached_documents']==1
    assert not seen


def test_extraction_timeout_saves_batches_and_returns_retryable_state(client,monkeypatch):
    import asyncio
    _,headers=create(client);entry=uploaded(client,headers,QUOTE)
    rows=[chunk(chunk_id=f'chunk{i}',doc_id=entry['doc_id'],version_id=entry['version_id']) for i in range(4)]
    monkeypatch.setattr(intel,'chunks_for',lambda entry:rows)
    monkeypatch.setattr(intel,'RULE_EXTRACTION_TIMEOUT',.1)
    monkeypatch.setattr(intel,'RULE_EXTRACTION_PAUSE',0)
    calls=0
    async def chat(messages,**kwargs):
        nonlocal calls
        calls+=1
        if calls==2:await asyncio.sleep(10)
        return LLMResponse(json.dumps({'rules':[raw(chunk_id='chunk0')]}),'fixture','fixture',1)
    monkeypatch.setattr(intel,'get_llm_client',lambda:SimpleNamespace(chat=chat))
    result=client.post('/personal/rules/extract',headers=headers,json={'document_id':entry['doc_id']}).json()
    assert result['status']=='partial' and result['errors'][0]['error']=='ExtractionTimeout'
    with institutions.scope(personal.resolve(headers['X-Workspace-ID'])):
        saved=next(iter(intel._cache().values()))
        assert saved['partial'] and len(saved['completed_chunk_ids'])==3 and len(saved['rules'])==1


def test_busy_extraction_fails_fast_without_provider_call(client,monkeypatch):
    _,headers=create(client)
    monkeypatch.setattr(intel,'_RULE_LOCK',SimpleNamespace(locked=lambda:True))
    chat=AsyncMock();monkeypatch.setattr(intel,'get_llm_client',lambda:SimpleNamespace(chat=chat))
    result=client.post('/personal/rules/extract',headers=headers,json={}).json()
    assert result['status']=='busy' and result['errors']
    chat.assert_not_called()
