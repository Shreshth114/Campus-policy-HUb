"""Prepared demo questions must use real scoped endpoints, never canned answers."""
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from fastapi.testclient import TestClient
from src import server, pipeline, intelligence
from tests.test_personal import client, create

QUESTIONS = ['I have 78% attendance because I was seriously ill. Can I get attendance condonation?', 'What documents are required if I miss an examination due to hospitalisation?', 'What happens if my attendance falls below the required threshold?', 'Who approves attendance condonation, and what is the application deadline?', 'Can I temporarily discontinue my programme due to medical problems?', 'Is 60% attendance enough if I have a medical certificate?', 'Can I apply for a make-up exam after 7 days of hospitalization?', 'Can I take unlimited medical breaks during B.Tech?']

@pytest.mark.parametrize('question',QUESTIONS)
@pytest.mark.parametrize('mode',['raw','hyde','fusion'])
def test_former_demo_questions_always_call_pipeline(client,monkeypatch,question,mode):
    _,headers=create(client)
    real=AsyncMock(return_value=SimpleNamespace(to_dict=lambda:{'decision':'abstained','answer':'pipeline sentinel'}))
    monkeypatch.setattr(pipeline,'ask',real)
    result=client.post('/personal/ask',headers=headers,json={'question':question,'mode':mode})
    assert result.status_code==200 and result.json()['answer']=='pipeline sentinel'
    real.assert_awaited_once_with(question,mode)

@pytest.mark.parametrize('mode',['raw','hyde','fusion'])
def test_empty_workspace_cannot_receive_nit_goa_policy(client,mode):
    _,headers=create(client)
    result=client.post('/personal/ask',headers=headers,json={'question':QUESTIONS[0],'mode':mode}).json()
    assert result['decision']=='abstained'
    assert result['retrieved']==[] and result['citations']==[]
    assert not result.get('citations_verified') and not result.get('demo_mode')


def test_prepared_comparison_route_and_auth_exception_removed(client):
    assert client.get('/personal/compare/prepared').status_code==404
    _,headers=create(client)
    assert client.get('/personal/compare/prepared',headers=headers).status_code==404
    assert client.get('/personal/versions').status_code==404
    assert client.get('/personal/versions',headers=headers).json()=={'versions':[]}


def test_version_comparison_uses_selected_documents(client,monkeypatch):
    _,headers=create(client)
    seen=[]
    def compare(**kwargs):
        seen.append(kwargs)
        return {'status':'blocked','message':'No extracted rules','changes':[]}
    monkeypatch.setattr(intelligence,'compare_versions',compare)
    body={'old_document_id':'a','old_version_id':'v1','new_document_id':'b','new_version_id':'v2'}
    result=client.post('/personal/changes',headers=headers,json=body)
    assert result.status_code==200 and result.json()['status']=='blocked'
    assert seen==[body]
