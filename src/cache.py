"""
cache.py — Semantic cache with exact-match primary and optional cosine similarity.

Design decision D-003: Exact normalized-string match is the default.
Semantic matching is opt-in (CACHE_SEMANTIC_ENABLED) with threshold >= 0.95.

Invalidation: when a document changes, entries citing that doc_id are deleted.
"""

import json
import re
import time
from typing import Optional

from src.config import CACHE_THRESHOLD, CACHE_SEMANTIC_ENABLED, CACHE_PATH
from src.persistence import CACHE_LOCK, INDEX_LOCK, write_json
from src.institutions import current, workspace_path
from functools import wraps


def cache_locked(fn):
    @wraps(fn)
    def locked(*args, **kwargs):
        with INDEX_LOCK, CACHE_LOCK:
            return fn(*args, **kwargs)
    return locked

# In-memory cache
_cache: list[dict] = []
_loaded = False


def _normalize_question(q: str) -> str:
    """Normalize a question for exact-match comparison."""
    import unicodedata
    q = unicodedata.normalize("NFKC", q).casefold().strip()
    # Preserve negation/apostrophes, numeric punctuation and operators.
    q = re.sub(r"[?!]+$", "", q)
    q = re.sub(r"\s+", " ", q)     # collapse whitespace
    return q


def _load_cache():
    """Load cache from disk if it exists."""
    global _cache, _loaded
    _cache = []
    if workspace_path('cache').exists():
        try:
            with open(workspace_path('cache')) as f:
                entries = json.load(f)
                _cache = [entry for entry in entries if isinstance(entry, dict)
                          and isinstance(entry.get("answer"), str)
                          and isinstance(entry.get("citations", []), list)] if isinstance(entries, list) else []
        except Exception:
            _cache = []
    _loaded = True


def _save_cache():
    """Persist cache to disk."""
    write_json(workspace_path('cache'), _cache)

@cache_locked
def cache_lookup(question: str, production: bool = True) -> Optional[dict]:
    """
    Look up a question in the cache.

    Returns cached entry dict with {answer, citations, similarity} or None.
    """
    _load_cache()
    normalized = _normalize_question(question)

    def eligible(entry):
        if entry.get("institution_id") != current().institution_id or entry.get("workspace_id", "") != current().workspace_id: return False
        if not production:
            return True
        from src.store import citation_fingerprint
        saved = entry.get("source_fingerprint")
        fingerprint = citation_fingerprint(entry.get("evidence_ids",entry.get("citations", [])))
        # Normalize tuple/list differences after JSON persistence.
        return saved is not None and fingerprint is not None and json.dumps(saved) == json.dumps(fingerprint)

    # Pass 1: exact normalized string match
    for entry in _cache:
        if entry.get("normalized_question") == normalized and eligible(entry):
            return {
                "answer": entry["answer"],
                "citations": entry.get("citations", []),
                "similarity": 1.0,
                "retrieved": entry.get("retrieved", []),
                "grounding_proof": entry.get("grounding_proof"),
            }

    # Pass 2: semantic similarity (if enabled)
    if CACHE_SEMANTIC_ENABLED and not production and _cache:
        from src.embeddings import embed_single
        import numpy as np

        q_embedding = embed_single(question)
        q_vec = np.array(q_embedding)

        best_sim = 0.0
        best_entry = None
        for entry in _cache:
            if "embedding" in entry and eligible(entry):
                cached_vec = np.array(entry["embedding"])
                # Cosine similarity
                sim = float(np.dot(q_vec, cached_vec) / (
                    np.linalg.norm(q_vec) * np.linalg.norm(cached_vec) + 1e-10
                ))
                if sim > best_sim:
                    best_sim = sim
                    best_entry = entry

        if best_entry and best_sim >= CACHE_THRESHOLD:
            return {
                "answer": best_entry["answer"],
                "citations": best_entry.get("citations", []),
                "similarity": round(best_sim, 4),
            }

    return None


@cache_locked
def cache_store(question: str, answer: str, citations: list[str],
                doc_ids: list[str], retrieved: list[dict] | None = None, grounding_proof: dict | None = None):
    """
    Store a question-answer pair in the cache.

    Args:
        question: Original question.
        answer: Generated answer.
        citations: List of cited chunk IDs.
        doc_ids: List of doc_ids of the cited source documents (for invalidation).
    """
    _load_cache()

    entry = {
        "workspace_id": current().workspace_id,
        "institution_id": current().institution_id,
        "question": question,
        "normalized_question": _normalize_question(question),
        "answer": answer,
        "citations": citations,
        "doc_ids": doc_ids,
        "timestamp": time.time(),
        "retrieved": retrieved or [],
        "grounding_proof": grounding_proof,
    }
    from src.store import citation_fingerprint
    entry['evidence_ids']=list(dict.fromkeys(cid for r in (retrieved or []) if r['chunk_id'] in citations for cid in (r.get('source_chunk_ids') or [r['chunk_id']]))) or citations
    entry["source_fingerprint"] = citation_fingerprint(entry['evidence_ids'])

    # Add embedding for semantic cache
    if CACHE_SEMANTIC_ENABLED:
        from src.embeddings import embed_single
        entry["embedding"] = embed_single(question)

    # Replace existing entry with same normalized question, or append
    normalized = entry["normalized_question"]
    _cache[:] = [e for e in _cache if e.get("normalized_question") != normalized]
    _cache.append(entry)

    _save_cache()


@cache_locked
def invalidate_by_doc_id(doc_id: str) -> int:
    """
    Remove all cache entries that cite the given doc_id.
    Called when a document is re-indexed.

    Returns number of entries removed.
    """
    _load_cache()
    before = len(_cache)
    _cache[:] = [
        e for e in _cache
        if doc_id not in e.get("doc_ids", []) and not any(c.get("doc_id")==doc_id for c in e.get("retrieved", []))
    ]
    removed = before - len(_cache)
    if removed > 0:
        _save_cache()
    return removed


@cache_locked
def clear_cache() -> int:
    """Clear the entire cache. Returns count cleared."""
    _load_cache()
    count = len(_cache)
    _cache.clear()
    _save_cache()
    return count


@cache_locked
def get_cache_stats() -> dict:
    """Return cache statistics."""
    _load_cache()
    return {
        "entries": len(_cache),
        "semantic_enabled": False,
        "experimental_semantic_enabled": CACHE_SEMANTIC_ENABLED,
        "threshold": CACHE_THRESHOLD,
    }

