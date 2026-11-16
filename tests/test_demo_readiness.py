import subprocess
from pathlib import Path
from tests.test_personal import client,create,uploaded

def test_demo_workspace_and_measured_indexing(client):
    response=client.post('/personal/demo',json={})
    assert response.status_code==200
    data=response.json();assert data['workspace']['synthetic_demo'] and 'SYNTHETIC' in data['workspace']['college']
    headers={'X-Workspace-ID':data['workspace']['workspace_id']}
    documents=client.get('/personal/documents',headers=headers).json()['documents']
    assert len(documents)==2 and all('SYNTHETIC' in d['original_filename'] and d['authority_status']=='pending' for d in documents)
    assert all(d['indexing_elapsed_s'] is not None for d in documents)
    assert client.get('/personal/evidence',headers=headers).json()['chunks']
    _,foreign=create(client)
    assert client.get('/personal/evidence',headers=foreign).json()['chunks']==[]


def test_session_metrics_use_only_observed_values():
    path=Path(__file__).resolve().parents[1]/'web/ui.js'
    code="""const assert=require('node:assert/strict'),m=require(process.argv[1]).SessionMetrics;assert.equal(m.summary().p95_ms,null);m.record({cache_hit:true,provider:'test',decision:'answered'},10);m.record({decision:'abstained'},30);const s=m.summary();assert.equal(s.requests,2);assert.equal(s.cache_hit_rate,.5);assert.equal(s.p50_ms,10);assert.equal(s.p95_ms,30);assert.equal(s.abstain_rate,.5);"""
    result=subprocess.run(['node','-e',code,str(path)],capture_output=True,text=True);assert result.returncode==0,result.stderr
