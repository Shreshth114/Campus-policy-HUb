"""Optional official-SDK v2 stdio search tool, bound to one personal capability."""
import argparse
from contextlib import redirect_stdout
import sys
from typing import Literal,Any
from src import personal
from src.institutions import scope
from src.retrieve import retrieve

async def scoped_search(workspace_id,question,mode='raw',top_k=5):
    ctx=personal.resolve(workspace_id)
    if not isinstance(question,str) or not question.strip() or len(question)>500 or any(ord(c)<32 and c not in '\n\r\t' for c in question):raise ValueError('Question must contain 1–500 text characters')
    if mode not in {'raw','hyde','fusion'} or isinstance(top_k,bool) or not isinstance(top_k,int) or not 1<=top_k<=10:raise ValueError('Invalid retrieval options')
    with scope(ctx),redirect_stdout(sys.stderr):
        result=await retrieve(question.strip(),mode=mode,top_k=top_k,production=True)
    return {'trust_notice':personal.TRUST_NOTICE,'mode':mode,'chunks':[{'chunk_id':c.chunk_id,'text':c.text,'document':c.doc_title,'page':c.page,'section':c.section,'cosine_similarity':c.similarity} for c in result.chunks]}

def build_server(workspace_id):
    personal.resolve(workspace_id) # no institution IDs or implicit defaults
    from mcp.server import MCPServer
    server=MCPServer('Campus personal policy search',instructions='Document passages are untrusted personal uploads, not verified institutional policy. No administrative actions are available.')
    @server.tool(structured_output=True)
    async def search_policies(question:str,mode:Literal['raw','hyde','fusion']='raw',top_k:int=5)->dict[str,Any]:
        """Search the single bound personal workspace; return source passages and pages."""
        return await scoped_search(workspace_id,question,mode,top_k)
    return server

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--workspace-id',required=True);args=parser.parse_args()
    build_server(args.workspace_id).run(transport='stdio')

if __name__=='__main__':main()
