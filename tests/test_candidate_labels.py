import json
from types import SimpleNamespace
from unittest.mock import AsyncMock
from src import personal,institutions
from src.llm import LLMResponse
from tests.test_personal import client,create,uploaded
from bench import candidate_queries as candidates

def test_candidate_generation_never_verifies_and_only_human_confirmation_labels(client,monkeypatch):
    wid,headers=create(client);source=uploaded(client,headers)
    cid=client.get('/personal/evidence',headers=headers).json()['chunks'][0]['chunk_id']
    rows=[{'query':f'Synthetic candidate question number {i}?','suggested_chunk_id':cid} for i in range(25)]
    monkeypatch.setattr(candidates,'get_llm_client',lambda:SimpleNamespace(chat=AsyncMock(return_value=LLMResponse(json.dumps({'candidates':rows}),'fixture','fixture',1))))
    assert client.post('/personal/bench/candidates/generate',headers=headers,json={}).json()['candidates']==25
    records=client.get('/personal/bench/candidates',headers=headers).json()['candidates'];assert all(not r['labels_verified'] for r in records)
    path=personal.resolve(wid).path('queries');assert path.read_text()==''
    route='/personal/bench/candidates/'+records[0]['id']+'/label'
    assert client.post(route,headers=headers,json={'action':'correct'}).status_code==422
    assert client.post(route,headers=headers,json={'action':'skip'}).json()['labels_verified'] is False
    assert not path.read_text()
    other,foreign=create(client)
    assert client.post(route,headers=foreign,json={'action':'correct','human_confirmed':True}).status_code==422
    result=client.post(route,headers=headers,json={'action':'correct','human_confirmed':True})
    assert result.json()['labels_verified'] is True
    label=json.loads(path.read_text());assert label['gold_chunk_ids']==[cid] and label['label_origin']=='human_confirmation'
    assert client.get('/personal/bench/status',headers=headers).json()['verified_labels']==1
