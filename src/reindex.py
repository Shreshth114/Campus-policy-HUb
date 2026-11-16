"""Stage changed files before short, locked index commits; never embed unchanged files."""
import json
import time
from pathlib import Path
from threading import Lock

from src.institutions import current as institution_context, workspace_path
from src.config import DATA_RAW_DIR, DATA_DECOYS_DIR, MANIFEST_PATH, DATA_PROCESSED_DIR
from src.ingest import ingest_file, _file_hash, _doc_id_from_path
from src.embeddings import embed_texts
from src.store import (upsert_chunks, delete_by_doc_id, get_collection_count,
                       get_collection, sync_authority_metadata)
from src.cache import invalidate_by_doc_id
from src.persistence import INDEX_LOCK, write_json

_REINDEX_LOCK = Lock()


def _load_manifest():
    if workspace_path('manifest').exists():
        value = json.loads(workspace_path('manifest').read_text())
        if not isinstance(value, dict):
            raise ValueError("Invalid index manifest")
        if 'files' in value:
            if value.get('institution_id')!=institution_context().institution_id or value.get('workspace_id','')!=institution_context().workspace_id: raise ValueError('Foreign index manifest')
            return value['files']
        return value  # historical in-workspace checkpoints, rewritten in scoped format on save
    return {}


def _save_manifest(manifest):
    from src.authority import get_registry
    entries=get_registry()
    documents=[{'document_id':did,'institution_id':institution_context().institution_id,'version_id':manifest[entry['source_path']],
                'file_hash':manifest[entry['source_path']],'source_path':entry['source_path']} for did,entry in entries.items() if entry['source_path'] in manifest]
    write_json(workspace_path('manifest'), {'workspace_id':institution_context().workspace_id,'institution_id':institution_context().institution_id,'files':manifest,'documents':documents})


def _scan_files():
    from src.authority import get_registry
    files={}
    for entry in get_registry().values():
        if entry.get('extraction_status') == 'removed': continue
        path=Path(entry['source_path'])
        if path.is_file(): files[str(path)]=(_file_hash(path),False)
    registered={str(Path(e['source_path'])) for e in get_registry().values()}
    historical={v.get('source_path') for e in get_registry().values() for v in (e.get('history') or [])}
    for path in sorted(workspace_path('raw').glob('*')):
        if path.is_file() and path.suffix.lower() in {'.pdf','.txt'} and str(path) not in registered|historical:
            files[str(path)]=(_file_hash(path),False)
    # Evaluation fixtures are separate and still institution-bound.
    for path in sorted(workspace_path('decoys').glob('*')):
        if path.is_file() and path.suffix.lower() in {'.txt','.pdf'}:
            files[str(path)]=(_file_hash(path),True)
    return files


def _replace_document(doc_id, chunks, embeddings):
    """Readers observe the old or new document, never a partly replaced one."""
    with INDEX_LOCK:
        from src.authority import get_registry
        entry=get_registry().get(doc_id)
        if chunks and entry and entry['version_id']!=chunks[0].version_id:
            raise ValueError('Document was replaced during embedding; retry current version')
        collection = get_collection()
        previous = collection.get(where={"$and": [{"doc_id": doc_id}, institution_context().filter]},
                                  include=["documents", "metadatas", "embeddings"])
        try:
            deleted = delete_by_doc_id(doc_id)
            if chunks:
                upsert_chunks([c.chunk_id for c in chunks], [c.text for c in chunks],
                              embeddings, [c.to_metadata() for c in chunks])
        except BaseException:
            # Ctrl+C during a commit must restore the previous document too.
            delete_by_doc_id(doc_id)
            if previous["ids"]:
                collection.upsert(ids=previous["ids"], documents=previous["documents"],
                                  embeddings=previous["embeddings"], metadatas=previous["metadatas"])
            raise
        return deleted


def reindex(document_id=None,force=False):
    with _REINDEX_LOCK:
        return _reindex(document_id,force)


def _reindex(document_id=None,force=False):
    started = time.perf_counter()
    print("[reindex] Reading manifest and hashing source files...", flush=True)
    old = _load_manifest()
    current = _scan_files()
    if document_id is not None:
        from src.authority import get_registry
        entry=get_registry().get(document_id)
        if not entry: raise ValueError('Unknown document in this institution')
        target=entry['source_path']
        current={p:v for p,v in current.items() if p==target}
        selected_old={p:v for p,v in old.items() if p==target}
    else:selected_old=old
    added = set(current) - set(selected_old)
    deleted = set(selected_old) - set(current)
    modified = {p for p in set(selected_old) & set(current) if old[p] != current[p][0]}
    if force and document_id and institution_context().personal:
        modified.update(set(current)&set(selected_old))
    unchanged = set(current) & set(old) - modified
    print(f"[reindex] Scan complete in {time.perf_counter() - started:.2f}s: "
          f"{len(added)} added, {len(modified)} modified, {len(deleted)} deleted, "
          f"{len(unchanged)} unchanged.", flush=True)
    manifest = dict(old)
    report = {"actions": {"added": sorted(added), "modified": sorted(modified),
                           "deleted": sorted(deleted), "unchanged": len(unchanged)},
              "chunks_added": 0, "chunks_deleted": 0, "cache_invalidated": 0,
              "errors": [], "documents": []}
    activity_path=workspace_path('processed')/'index_activity.json'
    activity={'institution_id':institution_context().institution_id,'status':'running','stage':'scan','completed':0,'total':len(added|modified|deleted),'documents':[]}
    write_json(activity_path,activity)
    pending = sorted(added | modified | deleted)
    for position, name in enumerate(pending, 1):
        path = Path(name)
        decoy = current[name][1] if name in current else path.parent == DATA_DECOYS_DIR
        doc_id = _doc_id_from_path(path, is_decoy=decoy)
        document_started = time.perf_counter()
        timings = {}
        stage = "parsing/chunking"
        print(f"[reindex] [{position}/{len(pending)}] {path.name}: "
              f"{'removing deleted source' if name in deleted else 'preparing source'}", flush=True)
        activity.update(file=path.name,stage=stage)
        write_json(activity_path,activity)
        try:
            chunks, embeddings = [], []
            if name not in deleted:
                stage_started = time.perf_counter()
                chunks = ingest_file(path, is_decoy=decoy)
                timings["parse_chunk_s"] = round(time.perf_counter() - stage_started, 3)
                if not chunks:
                    raise ValueError("No extractable text (possibly scanned/image-based); OCR is not implemented. Previous index retained")
                stage = "embedding"
                activity.update(stage=stage,chunks=len(chunks));write_json(activity_path,activity)
                stage_started = time.perf_counter()
                print(f"[reindex] {path.name}: embedding {len(chunks)} chunks...", flush=True)
                embeddings = embed_texts([c.text for c in chunks])
                timings["embed_s"] = round(time.perf_counter() - stage_started, 3)
                print(f"[reindex] {path.name}: embedding finished in {timings['embed_s']:.2f}s", flush=True)
                if len(embeddings) != len(chunks):
                    raise ValueError("Embedding count does not match chunks")
                if _file_hash(path) != current[name][0]:
                    raise ValueError("Source changed during indexing; retry")
            stage = "index commit"
            activity.update(stage=stage);write_json(activity_path,activity)
            stage_started = time.perf_counter()
            print(f"[reindex] {path.name}: committing index update...", flush=True)
            report["chunks_deleted"] += _replace_document(doc_id, chunks, embeddings)
            timings["commit_s"] = round(time.perf_counter() - stage_started, 3)
            report["chunks_added"] += len(chunks)
            stage = "cache/manifest persistence"
            stage_started = time.perf_counter()
            removed_cache=invalidate_by_doc_id(doc_id)
            report["cache_invalidated"] += removed_cache
            if institution_context().personal:
                rules_path=workspace_path('processed')/'rules.json'
                if rules_path.exists():
                    cache=json.loads(rules_path.read_text());cache={k:v for k,v in cache.items() if v.get('document_id')!=doc_id or v.get('file_hash')!=current[name][0]}
                    write_json(rules_path,cache)
            if name in deleted:
                manifest.pop(name, None)
            else:
                manifest[name] = current[name][0]
            _save_manifest(manifest)
            timings["persist_s"] = round(time.perf_counter() - stage_started, 3)
            from src.documents import set_index_status
            if not decoy and name not in deleted: set_index_status(doc_id, 'indexed', len(chunks),expected_version=current[name][0])
            timings["total_s"] = round(time.perf_counter() - document_started, 3)
            if institution_context().personal and name not in deleted:
                from src.authority import get_registry,_save_registry
                from src.persistence import AUTHORITY_LOCK
                with AUTHORITY_LOCK:
                    entries=get_registry();entries[doc_id].update(indexing_elapsed_s=timings['total_s'],cache_invalidated=removed_cache);_save_registry(entries)
            report["documents"].append({"file": path.name, "status": "ok", "timings_s": timings})
            print(f"[reindex] {path.name}: complete; {len(chunks)} chunks; "
                  f"{timings['total_s']:.2f}s total. Manifest saved.", flush=True)
        except Exception as exc:
            from src.documents import set_index_status
            if not decoy: set_index_status(doc_id, 'failed', error=f'{stage}: {type(exc).__name__}',expected_version=current[name][0] if name in current else None)
            report["errors"].append({"file": path.name, "stage": stage, "error": type(exc).__name__})
            print(f"[reindex] {path.name}: FAILED at {stage} ({type(exc).__name__}); "
                  "inspect the source and report; this file was not silently skipped.", flush=True)
        except KeyboardInterrupt:
            print(f"[reindex] Interrupted during {stage} for {path.name}; "
                  "completed documents keep their saved manifest entries. "
                  "Documents without a matching manifest checkpoint are retried on rerun.", flush=True)
            raise
        activity.update(completed=position,documents=report['documents'],errors=report['errors'])
        write_json(activity_path,activity)
    print("[reindex] Synchronizing source-approval flags and saving manifest...", flush=True)
    sync_authority_metadata()
    _save_manifest(manifest)
    report.update(total_chunks=get_collection_count(),
                  elapsed_s=round(time.perf_counter() - started, 3),
                  status="partial_failure" if report["errors"] else "ok")
    activity.update(status=report['status'],stage='complete',elapsed_s=report['elapsed_s']);write_json(activity_path,activity)
    return report


if __name__ == "__main__":
    import argparse
    from src.institutions import resolve, scope
    parser=argparse.ArgumentParser(); parser.add_argument('--institution-id', required=True)
    args=parser.parse_args()
    with scope(resolve(args.institution_id)): print(json.dumps(reindex(), indent=2))
