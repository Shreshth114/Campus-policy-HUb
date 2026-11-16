"""Real stdio MCP handshake/search in disposable personal storage (optional SDK v2)."""
import asyncio,json,os,sys
from pathlib import Path
from tempfile import TemporaryDirectory
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from mcp import Client,StdioServerParameters
from src import institutions,personal,store,documents
from src.institutions import scope
from src.ingest import ingest_file
from src.embeddings import embed_texts
from scripts.verify_personal_e2e import fixture

async def verify():
 with TemporaryDirectory(prefix='campus-mcp-check-') as temp:
  root=Path(temp);institutions.DATA_ROOT=root/'data';store.CHROMA_DIR=str(root/'legacy')
  entry=personal.create('SYNTHETIC TEST FIXTURE MCP')
  with scope(personal.resolve(entry['workspace_id'])):
   source=documents.upload('SYNTHETIC TEST FIXTURE.pdf',fixture());chunks=ingest_file(Path(source['source_path']))
   store.upsert_chunks([c.chunk_id for c in chunks],[c.text for c in chunks],embed_texts([c.text for c in chunks]),[c.to_metadata() for c in chunks]);documents.set_index_status(source['doc_id'],'indexed',len(chunks))
  bootstrap="from pathlib import Path;import os;from src import institutions,store;institutions.DATA_ROOT=Path(os.environ['MCP_CHECK_ROOT'])/'data';store.CHROMA_DIR=str(Path(os.environ['MCP_CHECK_ROOT'])/'legacy');from src.mcp_server import main;main()"
  params=StdioServerParameters(command=sys.executable,args=['-c',bootstrap,'--workspace-id',entry['workspace_id']],env={'MCP_CHECK_ROOT':str(root),'PYTHONPATH':os.environ.get('PYTHONPATH',''),'HF_HUB_OFFLINE':'1','TMPDIR':os.getenv('TMPDIR','/tmp')})
  async with Client(params) as client:
   tools=await client.list_tools();assert [t.name for t in tools.tools]==['search_policies']
   response=await client.call_tool('search_policies',{'question':'What attendance is required?','mode':'raw','top_k':3})
   assert not response.is_error
   data=response.structured_content
   if data is None:data=json.loads(response.content[0].text)
   if 'result' in data:data=data['result']
   assert data['chunks'] and data['chunks'][0]['page']==1 and 'source_path' not in str(data) and entry['workspace_id'] not in str(data)
   print(json.dumps({'transport':'stdio','tool':'search_policies','chunks':len(data['chunks']),'page':data['chunks'][0]['page'],'scope':'disposable personal fixture','protocol_verified':True}))

if __name__=='__main__':asyncio.run(verify())
