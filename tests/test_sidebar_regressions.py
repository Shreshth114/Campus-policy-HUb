import json
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest
from src import intelligence,personal
from src.llm import LLMResponse
from tests.test_personal import client,create,uploaded
from bench import candidate_queries

@pytest.mark.parametrize('wrapped',[False,True])
def test_candidate_sidebar_accepts_plain_or_wrapped_array_without_verifying(client,monkeypatch,wrapped):
    wid,headers=create(client);uploaded(client,headers)
    cid=client.get('/personal/evidence',headers=headers).json()['chunks'][0]['chunk_id']
    rows=[{'query':f'Synthetic candidate {i}?','suggested_chunk_id':cid} for i in range(25)]
    payload={'candidates':rows} if wrapped else rows
    monkeypatch.setattr(candidate_queries,'get_llm_client',lambda:SimpleNamespace(chat=AsyncMock(return_value=LLMResponse(json.dumps(payload),'fixture','fixture',1))))
    response=client.post('/personal/bench/candidates/generate',headers=headers,json={})
    assert response.status_code==200
    assert response.json()['candidates']==25
    assert not personal.resolve(wid).path('queries').read_text()
    assert all(not row['labels_verified'] for row in client.get('/personal/bench/candidates',headers=headers).json()['candidates'])


def test_parser_preserves_plain_arrays_and_existing_fenced_objects():
    assert intelligence.parse_json('[{"question":"a"},{"question":"b"}]')==[{'question':'a'},{'question':'b'}]
    assert intelligence.parse_json('```json\n{"rules":[]}\n```')=={'rules':[]}


def test_sidebar_workspace_clearing_and_stale_responses():
    import subprocess
    from pathlib import Path
    script=Path(__file__).with_name('sidebar_frontend.test.cjs')
    result=subprocess.run(['node',str(script)],capture_output=True,text=True,timeout=20)
    assert result.returncode==0,result.stderr
