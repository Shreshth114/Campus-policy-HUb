"""Disposable zero-provider demo. Open http://localhost:8028/fixture/start."""
import asyncio
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))


def main():
    import pymupdf
    import uvicorn
    from fastapi.responses import HTMLResponse
    from src import server,personal,institutions,documents,reindex,store,intelligence,llm,answer,hyde
    from src.persistence import write_json

    calls={'provider_calls':0}
    def forbidden(*args,**kwargs):
        calls['provider_calls']+=1
        raise AssertionError('Provider access is disabled in this synthetic demo')
    for module in (llm,intelligence,answer,hyde):
        module.get_llm_client=forbidden
    llm.GroqProvider.chat=forbidden
    llm.GeminiProvider.chat=forbidden

    async def fixture_analysis(question,facts,confirmed,applicability_confirmed=False):
        if not confirmed:raise ValueError('Confirm facts first')
        result=intelligence.evaluate(intelligence.list_rules(),facts,applicability_confirmed)
        return {**result,'question':question,'explanations':[],'trust_notice':personal.TRUST_NOTICE}
    # The setup analysis uses fixture rules directly, avoiding its optional LLM explanation.
    intelligence.analyse=fixture_analysis

    with tempfile.TemporaryDirectory(prefix='whatif-demo-') as folder:
        root=Path(folder)
        institutions.DATA_ROOT=root/'data'
        store.CHROMA_DIR=str(root/'chroma')
        server.RATE_LIMIT=10000
        entry=personal.create('SYNTHETIC TEST FIXTURE',synthetic_demo=True)
        ctx=personal.resolve(entry['workspace_id'])
        with institutions.scope(ctx):
            pdf=pymupdf.open()
            pdf.new_page().insert_text((40,60),'SYNTHETIC TEST FIXTURE. Minimum completion is at least 75 percent.')
            source=documents.upload('SYNTHETIC TEST FIXTURE.pdf',pdf.tobytes())
            pdf.close()
            reindex.embed_texts=lambda texts:[[1.,0.] for _ in texts]
            reindex.reindex()
            source=intelligence.document_entry(source['doc_id'])
            chunk=intelligence.chunks_for(source)[0]
            rule=intelligence.validate_rule({'subject':'completion','operator':'>=','value':75,'unit':'%',
                'verbatim_quote':'Minimum completion is at least 75 percent.','exceptions':[]},chunk)
            if not rule:raise RuntimeError('Synthetic rule verification failed')
            write_json(ctx.processed/'rules.json',{intelligence._key(source):{'rules':[rule]}})

        @server.app.get('/fixture/start')
        async def start():
            # Capability is delivered only to this local disposable demo's page.
            value=json.dumps(entry['workspace_id'])
            return HTMLResponse('<script>localStorage.setItem("campus-personal-workspace",'+value+');location.replace("/");</script>')

        @server.app.get('/fixture-provider-audit')
        async def audit():return calls

        print('SYNTHETIC TEST FIXTURE: open http://localhost:8028/fixture/start',flush=True)
        uvicorn.run(server.app,host='127.0.0.1',port=8028,access_log=False,log_level='warning')


if __name__=='__main__':main()
