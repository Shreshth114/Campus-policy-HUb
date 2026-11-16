"""Explicit human approval bound to a source file's SHA-256 content hash."""
import hashlib
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from src.config import DATA_PROCESSED_DIR
from src.institutions import current, workspace_path
from src.persistence import AUTHORITY_LOCK, write_json

REGISTRY_PATH = DATA_PROCESSED_DIR / "source_registry.json"


@dataclass
class SourceEntry:
    doc_id: str
    doc_title: str
    institution: str
    authority_status: str
    effective_date: Optional[str] = None
    source_url: Optional[str] = None
    source_path: Optional[str] = None
    added_at: Optional[float] = None
    approved_at: Optional[float] = None
    notes: Optional[str] = None
    file_hash: Optional[str] = None
    is_synthetic: bool = False
    workspace_id: str = ""
    trust_level: str = "institutional"
    page_count: int = 0
    extraction_profile: str = "legacy"
    indexing_elapsed_s: float | None = None
    cache_invalidated: int = 0
    institution_id: str = ""
    version_id: str = ""
    original_filename: str = ""
    issuing_authority: Optional[str] = None
    programme: Optional[str] = None
    cohort: Optional[str] = None
    reviewer: Optional[str] = None
    extraction_status: str = "pending"
    extraction_error: Optional[str] = None
    chunk_count: int = 0
    history: Optional[list] = None


def source_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _load_registry():
    try:
        value = json.loads(workspace_path('registry').read_text())
        if not isinstance(value, dict):
            return {}
        valid = {}
        for key, entry in value.items():
            try:
                source = SourceEntry(**entry)
                if current().owns(source) and source.doc_id == key and source.authority_status in {"pending", "approved", "rejected"}:
                    valid[key] = asdict(source)
            except (TypeError, ValueError):
                continue
        return valid
    except (OSError, ValueError):
        return {}  # Fail closed: malformed approval data never grants access.


def _save_registry(registry):
    write_json(workspace_path('registry'), registry)


def register_source(doc_id, doc_title, institution="", source_path="",
                    effective_date=None, source_url=None, notes=None, is_synthetic=False):
    with AUTHORITY_LOCK:
        registry = _load_registry()
        digest = source_hash(source_path) if source_path and Path(source_path).is_file() else None
        old = registry.get(doc_id)
        if old and old.get("source_path") == source_path and old.get("file_hash") == digest and old.get("is_synthetic", False) == is_synthetic:
            return SourceEntry(**old)
        entry = SourceEntry(
            doc_id, doc_title, institution, "pending", effective_date,
            source_url, source_path, time.time(), notes=notes,
            file_hash=digest, is_synthetic=is_synthetic,
        )
        entry.institution_id = current().institution_id
        entry.workspace_id = current().workspace_id
        entry.trust_level = "personal_unverified" if current().personal else "institutional"
        entry.version_id = digest or ""
        entry.original_filename = Path(source_path).name
        entry.history = ((old.get('history') or []) + [{k:v for k,v in old.items() if k!='history'}]) if old else []
        registry[doc_id] = asdict(entry)
        _save_registry(registry)
        return entry


def approve_source(doc_id):
    """Human approval only; synthetic sources cannot be approved for production."""
    if current().personal:return False
    with AUTHORITY_LOCK:
        registry = _load_registry()
        entry = registry.get(doc_id)
        if not entry or entry.get("is_synthetic") or entry.get("extraction_status") != "indexed":
            return False
        path = entry.get("source_path")
        if not path or not Path(path).is_file() or source_hash(path) != entry.get("file_hash"):
            return False
        entry.update(authority_status="approved", approved_at=time.time())
        _save_registry(registry)
        return True


def reject_source(doc_id):
    with AUTHORITY_LOCK:
        registry = _load_registry()
        if doc_id not in registry:
            return False
        registry[doc_id].update(authority_status="rejected", approved_at=None)
        _save_registry(registry)
        return True


def get_registry():
    with AUTHORITY_LOCK:
        return _load_registry()


def approved_sources():
    """Check current content too: edits revoke eligibility before reindexing."""
    eligible = {}
    for doc_id, entry in get_registry().items():
        if entry.get("authority_status") != "approved" or entry.get("is_synthetic"):
            continue
        try:
            if entry.get("file_hash") and source_hash(entry["source_path"]) == entry["file_hash"]:
                eligible[doc_id] = entry
        except (OSError, KeyError, TypeError):
            continue
    return eligible


def is_approved(doc_id):
    return doc_id in approved_sources()


def get_status(doc_id):
    entry = get_registry().get(doc_id)
    return entry.get("authority_status") if entry else None


def get_approved_doc_ids():
    return set(approved_sources())


def clear_registry():
    with AUTHORITY_LOCK:
        _save_registry({})


def eligible_sources():
    """Personal upload eligibility is separate from institutional human approval."""
    if not current().personal:return approved_sources()
    result={}
    for did,entry in get_registry().items():
        if entry['extraction_status']!='indexed' or entry['authority_status']=='rejected' or entry['is_synthetic']:continue
        try:
            if source_hash(entry['source_path'])==entry['version_id']==entry['file_hash']:result[did]=entry
        except OSError:pass
    return result
