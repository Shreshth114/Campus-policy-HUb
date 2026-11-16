"""Anonymous capability workspaces; possession of the random ID grants local access."""
import json
import os
import secrets
import re
import shutil
import time
from pathlib import Path
from threading import RLock
from src import institutions
from src.persistence import write_json, INDEX_LOCK

LOCK=RLock()
TRUST_NOTICE='Based on documents you uploaded. Not verified by your institution.'
MAX_BYTES=int(os.getenv('PERSONAL_MAX_FILE_MB','30'))*1024*1024
MAX_PAGES=int(os.getenv('PERSONAL_MAX_PAGES','200'))
MAX_DOCUMENTS=int(os.getenv('PERSONAL_MAX_DOCUMENTS','20'))
if min(MAX_BYTES,MAX_PAGES,MAX_DOCUMENTS)<1:raise ValueError('Personal upload limits must be positive')

def registry():
    path=institutions.DATA_ROOT/'personal_workspaces.json'
    return json.loads(path.read_text()) if path.exists() else {}

def create(college='',synthetic_demo=False):
    with LOCK:
        wid=secrets.token_urlsafe(32)
        entry={'workspace_id':wid,'college':college.strip()[:160],'created_at':time.time(),'trust_level':'personal_unverified','synthetic_demo':synthetic_demo}
        ctx=institutions.InstitutionContext('',institutions.DATA_ROOT/'personal'/wid,workspace_id=wid)
        for path in (ctx.raw,ctx.processed,ctx.path('results'),ctx.path('decoys')):path.mkdir(parents=True,exist_ok=True)
        for key,value in [('registry',{}),('manifest',{}),('cache',[]),('hyde',{})]:write_json(ctx.path(key),value)
        ctx.path('queries').write_text('')
        entries=registry();entries[wid]=entry;write_json(institutions.DATA_ROOT/'personal_workspaces.json',entries)
        return entry

def resolve(wid):
    if not isinstance(wid,str) or not re.fullmatch(r'[A-Za-z0-9_-]{43}',wid) or wid not in registry():raise ValueError('A valid personal workspace ID is required')
    return institutions.InstitutionContext('',institutions.DATA_ROOT/'personal'/wid,workspace_id=wid)

def delete():
    ctx=institutions.current()
    if not ctx.personal:raise ValueError('Personal workspace required')
    with INDEX_LOCK,LOCK:
        from src.store import get_collection
        collection=get_collection();rows=collection.get(where=ctx.filter,include=[])
        if rows['ids']:collection.delete(ids=rows['ids'])
        root=(institutions.DATA_ROOT/'personal').resolve()
        if not ctx.root.resolve().is_relative_to(root):raise ValueError('Invalid workspace path')
        shutil.rmtree(ctx.root)
        entries=registry();entries.pop(ctx.workspace_id,None);write_json(institutions.DATA_ROOT/'personal_workspaces.json',entries)
        return {'deleted':True}
