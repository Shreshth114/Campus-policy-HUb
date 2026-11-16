#!/usr/bin/env python3
"""Opt-in live Groq/embedding/API verification in a disposable, isolated app instance.

Synthetic PDFs emulate reviewed source states ONLY inside the temporary instance.
No production registry, vector collection, approval or credential is modified.
"""
import argparse
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
from tempfile import TemporaryDirectory
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import httpx
import pymupdf
from src.config import PROJECT_ROOT

CHILD = r'''
import json,os
from pathlib import Path
from src import institutions,store,server,answer
import src.retrieve as retrieval
root=Path(os.environ['E2E_TEMP_ROOT'])
institutions.DATA_ROOT=root/'data'
store.CHROMA_DIR=str(root/'legacy-chroma')
original_hyde=retrieval.generate_hyde
last_hyde=None
audit={'answer_prompts_checked':0,'hyde_calls':0,'hyde_structurally_isolated':True}
async def observed_hyde(question):
    global last_hyde
    result=await original_hyde(question)
    last_hyde=result[0];audit['hyde_calls']+=1
    (root/'prompt-audit.json').write_text(json.dumps(audit))
    return result
retrieval.generate_hyde=observed_hyde
original_prompt=answer._build_answer_prompt
def observed_prompt(question,chunks):
    messages=original_prompt(question,chunks)
    text='\n'.join(m['content'] for m in messages)
    assert question in text
    assert all(c.text in text or __import__('html').escape(c.text,quote=False) in text for c in chunks)
    assert not last_hyde or last_hyde not in text
    audit['answer_prompts_checked']+=1
    (root/'prompt-audit.json').write_text(json.dumps(audit))
    return messages
answer._build_answer_prompt=observed_prompt
import uvicorn
uvicorn.run(server.app,host='127.0.0.1',port=int(os.environ['E2E_PORT']),access_log=False,log_level='warning')
'''

def make_pdf():
    pdf=pymupdf.open();page=pdf.new_page()
    page.insert_textbox((40,40,550,600),
        'SYNTHETIC TEST FIXTURE - NOT A UNIVERSITY POLICY\n'
        'Isolated Fixture College Laboratory Procedure\n\n'
        'In this fictional test procedure, a student requesting laboratory access must submit '
        'Form ZEBRA-42 to the fictional laboratory coordinator at least three working days before the visit. '
        'Access requires written approval from that coordinator. This fixture grants no real campus permissions.',fontsize=12)
    return pdf.tobytes()

def verify():
    with TemporaryDirectory(prefix='campus-live-e2e-') as directory:
        root=Path(directory);token=secrets.token_urlsafe(32)
        with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        env={**os.environ,'E2E_TEMP_ROOT':str(root),'E2E_PORT':str(port),'ADMIN_API_TOKEN':token,'HF_HUB_OFFLINE':'1'}
        log=(root/'server.log').open('w')
        process=subprocess.Popen([sys.executable,'-u','-c',CHILD],cwd=PROJECT_ROOT,env=env,stdout=log,stderr=log)
        report={'scope':'disposable_synthetic_review_state_emulation','real_university_policy_claim':False,'production_data_modified':False}
        try:
            with httpx.Client(base_url=f'http://127.0.0.1:{port}',timeout=180) as client:
                for attempt in range(100):
                    if process.poll() is not None:raise RuntimeError('Isolated server failed to start; inspect local verification log')
                    try:
                        if client.get('/health').status_code==200:break
                    except httpx.ConnectError:pass
                    time.sleep(.2)
                else:raise RuntimeError('Isolated server startup timeout')
                headers={'Authorization':'Bearer '+token}
                def admin(method,path,**kwargs):
                    response=client.request(method,path,headers=headers,**kwargs)
                    if not response.is_success:raise RuntimeError(f'Admin {method} {path}: HTTP {response.status_code}')
                    return response.json()
                report['unauthenticated_admin_status']=client.get('/admin/institutions').status_code
                a=admin('POST','/admin/institutions',json={'name':'ISOLATED SYNTHETIC Fixture College A'})
                b=admin('POST','/admin/institutions',json={'name':'ISOLATED SYNTHETIC Fixture College B'})
                base='/admin/institutions/'+a['institution_id']
                assert len(admin('GET','/admin/institutions')['institutions'])==2
                source=admin('POST',base+'/documents',files={'files':('synthetic-fixture.pdf',make_pdf(),'application/pdf')})['documents'][0]['source']
                did=source['doc_id'];assert source['authority_status']=='pending'
                indexed=admin('PATCH',base+'/sources/'+did+'/reindex-current',json={})
                assert indexed['status']=='ok' and indexed['chunks_added']>0
                detail=admin('GET',base+'/sources/'+did);assert detail['source']['authority_status']=='pending' and detail['chunks']
                assert detail['pages'][0]['page']==1 and 'ZEBRA-42' in detail['pages'][0]['text']
                review={'version_id':source['version_id'],'reviewer':'Authorised isolated fixture verifier','source_url':'https://example.invalid/synthetic-fixture','issuing_authority':'Fictional test authority - not a university','notes':'Synthetic review-state emulation in disposable test application only. Never a production policy.'}
                admin('POST',base+'/sources/'+did+'/approve',json=review)
                admin('PATCH',base,json={'published':True})
                public=client.get('/institutions').json()['institutions'];assert [i['institution_id'] for i in public]==[a['institution_id']]
                question='In this fictional laboratory procedure, which form is required, when must I submit it, and whose written approval is needed?'
                traces={};cache_verified=False
                for mode in ('raw','hyde','fusion'):
                    admin('POST',base+'/cache/clear',json={})
                    response=client.post('/ask',json={'institution_id':a['institution_id'],'question':question,'mode':mode})
                    response.raise_for_status();trace=response.json();traces[mode]=trace
                    assert trace['provider']=='groq' and trace['retrieved'] and not trace.get('error')
                    if trace['decision']=='answered':
                        assert trace['citations'] and 'ZEBRA' in trace['answer'].upper()
                        cached=client.post('/ask',json={'institution_id':a['institution_id'],'question':question,'mode':mode}).json()
                        assert cached['cache_hit'];cache_verified=True
                    else:
                        assert trace['abstain_reason']=='citation_check_failed' and not trace['citations']
                    assert all(c['institution_id']==a['institution_id'] and c['approved'] for c in trace['retrieved'])
                    for cid in trace['citations']:
                        citation=client.get('/institutions/'+a['institution_id']+'/citations/'+cid);citation.raise_for_status()
                        data=citation.json();assert data['page']==1 and data['doc_id']==did and 'ZEBRA-42' in data['text']
                assert any(t.get('hyde_text') and not t['hyde_failed'] for t in (traces['hyde'],traces['fusion']))
                assert traces['fusion']['retrieved'][0]['rrf_score'] is not None
                assert cache_verified
                unsupported=client.post('/ask',json={'institution_id':a['institution_id'],'question':'What is the melting point of tungsten?','mode':'raw'}).json();assert unsupported['decision']=='abstained'
                # Foreign workspace cannot inspect or mutate this source; publication has no implicit cross-tenant effect.
                foreign='/admin/institutions/'+b['institution_id']+'/sources/'+did
                assert client.get(foreign,headers=headers).status_code==404
                assert client.post(foreign+'/approve',headers=headers,json=review).status_code==409
                assert client.post('/ask',json={'institution_id':b['institution_id'],'question':question}).status_code==422
                admin('POST',base+'/sources/'+did+'/pending',json=review)
                revoked=client.post('/ask',json={'institution_id':a['institution_id'],'question':question,'mode':'raw'}).json()
                assert not revoked['cache_hit'] and revoked['decision']=='abstained'
                report.update(uploaded_documents=1,indexed_chunks=indexed['chunks_added'],pending_inspection=True,explicit_fixture_review=True,publication=True,
                    modes={mode:{'decision':t['decision'],'abstain_reason':t['abstain_reason'],'provider':t['provider'],'hyde_failed':t['hyde_failed'],'citation_pages':[c['page'] for c in t['retrieved']],'timings_ms':t['timings_ms'],'llm_usage':t['llm_usage']} for mode,t in traces.items()},
                    status='completed' if all(t['decision']=='answered' for t in traces.values()) else 'completed_with_guard_abstentions',
                    cache_hit_revalidated=cache_verified,revocation_invalidates_cache=True,unsupported_question=unsupported['abstain_reason'],foreign_access_rejected=True,
                    prompt_audit=json.loads((root/'prompt-audit.json').read_text()))
                return report
        finally:
            process.terminate()
            try:process.wait(timeout=10)
            except subprocess.TimeoutExpired:process.kill();process.wait()
            log.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--live',required=True,action='store_true');parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=verify()
    if args.output:args.output.write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))
