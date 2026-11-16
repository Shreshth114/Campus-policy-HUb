"""Scoped immutable original versions and hash-bound administrative review."""
import hashlib
import time
import uuid
from pathlib import Path
from dataclasses import asdict
from src.institutions import current, workspace_path
from src.authority import get_registry, _save_registry, register_source, source_hash
from src.persistence import AUTHORITY_LOCK, INDEX_LOCK, write_json

MAX_FILE_BYTES=30*1024*1024

def upload(filename, content, document_id=None):
    if not filename or len(filename)>200 or Path(filename).name != filename or '\\' in filename or not filename.lower().endswith('.pdf'):
        raise ValueError('A safe PDF filename is required')
    limit=__import__('src.personal',fromlist=['MAX_BYTES']).MAX_BYTES if current().personal else MAX_FILE_BYTES
    if not content or len(content)>limit or not content.startswith(b'%PDF-'):
        raise ValueError(f'Expected a PDF up to {limit//1024//1024} MB')
    pages=0
    if current().personal:
        from src import personal
        import pymupdf
        if len(content)>personal.MAX_BYTES:raise ValueError(f'PDF exceeds {personal.MAX_BYTES//1024//1024} MB')
        try:
            with pymupdf.open(stream=content,filetype='pdf') as pdf:
                if pdf.needs_pass:raise ValueError('Encrypted PDFs are not supported')
                pages=len(pdf)
                if not pages or pages>personal.MAX_PAGES:raise ValueError(f'PDF must have 1–{personal.MAX_PAGES} pages')
        except (pymupdf.FileDataError,RuntimeError):raise ValueError('Invalid PDF content')
    with INDEX_LOCK, AUTHORITY_LOCK:
        registry=get_registry()
        if current().personal and not document_id and sum(e['extraction_status']!='removed' for e in registry.values())>=personal.MAX_DOCUMENTS:
            raise ValueError(f'Workspace limit is {personal.MAX_DOCUMENTS} documents')
        if document_id and document_id not in registry: raise ValueError('Unknown document in this institution')
        owner=('p-'+hashlib.sha256(current().workspace_id.encode()).hexdigest()[:24]) if current().personal else current().institution_id
        did=document_id or f'{owner}:{uuid.uuid4()}'
        digest=hashlib.sha256(content).hexdigest()
        old=registry.get(did)
        if old and old['file_hash']==digest: return old
        path=workspace_path('raw')/did.split(':')[-1]/digest/filename
        path.parent.mkdir(parents=True,exist_ok=True)
        temp=path.with_suffix('.upload');temp.write_bytes(content);temp.replace(path)
        entry=register_source(did,Path(filename).stem,source_path=str(path))
        if current().personal:
            registry=get_registry();registry[did]['page_count']=pages;_save_registry(registry);entry.page_count=pages
        from src.cache import invalidate_by_doc_id
        invalidate_by_doc_id(did)
        if old:
            from src.reindex import _load_manifest,_save_manifest
            values=_load_manifest();values.pop(old['source_path'],None);_save_manifest(values)
        return asdict(entry)

def set_index_status(did,status,count=0,error=None,expected_version=None):
    with AUTHORITY_LOCK:
        entries=get_registry()
        if did in entries and (expected_version is None or entries[did]['version_id']==expected_version):
            entries[did].update(extraction_status=status,chunk_count=count,extraction_error=error)
            if current().personal and status=='indexed':entries[did]['extraction_profile']='personal_v2'
            _save_registry(entries)

def review(did,version_id,status,metadata):
    if current().personal:raise ValueError('Personal uploads cannot become institutional approvals')
    allowed={'source_url','issuing_authority','programme','cohort','effective_date','reviewer','notes'}
    if status not in {'pending','approved','rejected'} or set(metadata)-allowed: raise ValueError('Invalid review')
    with INDEX_LOCK, AUTHORITY_LOCK:
        entries=get_registry(); entry=entries.get(did)
        if not entry or entry['version_id']!=version_id: raise ValueError('Current document version required')
        if source_hash(entry['source_path']) != version_id: raise ValueError('File changed; upload a new version')
        if status=='approved' and (entry.get('is_synthetic') or entry.get('extraction_status')!='indexed'):
            raise ValueError('Only successfully indexed real documents may be approved')
        if not metadata.get('reviewer','').strip(): raise ValueError('Reviewer identity is required')
        if status=='approved' and (not metadata.get('source_url') or not metadata.get('issuing_authority')):
            raise ValueError('Approval requires a verified source URL and issuing authority')
        url=metadata.get('source_url')
        if url and not url.startswith(('https://','http://')): raise ValueError('Source URL must use HTTP or HTTPS')
        event={'status':status,'version_id':version_id,'at':time.time(),**metadata}
        entry.setdefault('history',[])
        entry['history']=(entry['history'] or [])+[event]
        entry.update(metadata,authority_status=status,approved_at=time.time() if status=='approved' else None)
        _save_registry(entries)
        from src.store import sync_authority_metadata
        from src.cache import invalidate_by_doc_id
        sync_authority_metadata();invalidate_by_doc_id(did)
        return entry

def remove(did):
    with INDEX_LOCK, AUTHORITY_LOCK:
        entries=get_registry()
        if did not in entries: raise ValueError('Unknown document')
        entry=entries[did];entry.update(authority_status='rejected',extraction_status='removed',approved_at=None)
        if current().personal:entries.pop(did)
        _save_registry(entries)
        from src.store import delete_by_doc_id
        from src.cache import invalidate_by_doc_id
        delete_by_doc_id(did);invalidate_by_doc_id(did)
        from src.reindex import _load_manifest,_save_manifest
        values=_load_manifest();values.pop(entry['source_path'],None);_save_manifest(values)
        if current().personal:
            import shutil,json
            directory=(current().raw/did.split(':')[-1]).resolve()
            if not directory.is_relative_to(current().raw.resolve()):raise ValueError('Invalid document location')
            if directory.exists():shutil.rmtree(directory)
            rule_path=current().processed/'rules.json'
            if rule_path.exists():
                cache=json.loads(rule_path.read_text())
                cache={k:v for k,v in cache.items() if v.get('document_id')!=did and not any(r.get('document_id')==did for r in v.get('rules',[]))}
                write_json(rule_path,cache)
        return {'removed':did,'original_retained':not current().personal}
