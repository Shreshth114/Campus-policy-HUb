"""
store.py — ChromaDB wrapper for vector storage.

Handles: collection management, upsert, delete by doc_id,
query with similarity score normalization.

Key design decision (D-002): ChromaDB returns cosine *distance*.
We convert to similarity: `similarity = 1.0 - distance`.
"""

from __future__ import annotations

import chromadb
import math
import time
from pathlib import Path
from chromadb.config import Settings
from dataclasses import dataclass, field

from src.config import CHROMA_DIR, TOP_K
from src.institutions import current
from src.authority import approved_sources, eligible_sources
from src.persistence import INDEX_LOCK
from functools import wraps


def index_locked(fn):
    @wraps(fn)
    def locked(*args, **kwargs):
        with INDEX_LOCK:
            return fn(*args, **kwargs)
    return locked


_client: chromadb.PersistentClient | None = None
_collection = None

COLLECTION_NAME = "institution_policy_chunks_v2"


@dataclass
class RetrievedChunk:
    """A chunk returned from vector search with metadata and score."""
    chunk_id: str
    text: str
    doc_id: str
    doc_title: str
    section: str
    page: int
    chunk_index: int
    similarity: float       # cosine similarity: 1.0 = identical, 0.0 = orthogonal
    workspace_id: str = ""
    institution_id: str = ""
    version_id: str = ""
    is_decoy: bool = False
    approved: bool = False
    rrf_score: float | None = None  # set only in fusion mode; separate from similarity
    is_synthetic: bool = False
    extraction_method: str = "unknown"
    source_chunk_ids: list[str] = field(default_factory=list)
    pages: list[int] = field(default_factory=list)

    @property
    def text_preview(self) -> str:
        """First 200 chars for display."""
        from src.evidence import relevant_sentence
        return relevant_sentence(self.text,'')


def _get_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=str(Path(CHROMA_DIR).with_name(".chroma-institutions")),
            settings=Settings(anonymized_telemetry=False),
        )
    return _client


@index_locked
def get_collection():
    """Get or create the policy chunks collection."""
    global _collection
    if _collection is None:
        client = _get_client()
        _collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
            embedding_function=None,  # All embeddings come from our explicit wrapper.
        )
    return _collection


def normalize_score(distance: float) -> float:
    """
    Convert cosine distance to similarity.

    ChromaDB cosine distance: 0 = identical, 2 = opposite.
    Similarity = 1.0 - distance.
    Clamped to [0, 1] for safety.
    """
    return max(0.0, min(1.0, 1.0 - distance)) if math.isfinite(distance) else 0.0


@index_locked
def upsert_chunks(chunk_ids: list[str], texts: list[str],
                  embeddings: list[list[float]], metadatas: list[dict]):
    """Upsert chunks into ChromaDB. Idempotent by chunk_id."""
    from types import SimpleNamespace
    if any(not current().owns(SimpleNamespace(workspace_id=m.get('workspace_id',''),institution_id=m.get('institution_id',''))) for m in metadatas):
        raise ValueError('Foreign chunk ownership')
    collection = get_collection()
    # ChromaDB has a batch size limit; process in batches of 100
    batch_size = 100
    for i in range(0, len(chunk_ids), batch_size):
        end = min(i + batch_size, len(chunk_ids))
        started = time.perf_counter()
        print(f"[store] Upserting chunks {i + 1}-{end}/{len(chunk_ids)}...", flush=True)
        collection.upsert(
            ids=chunk_ids[i:end],
            documents=texts[i:end],
            embeddings=embeddings[i:end],
            metadatas=metadatas[i:end],
        )
        print(f"[store] Upserted {end}/{len(chunk_ids)} chunks; "
              f"batch took {time.perf_counter() - started:.2f}s", flush=True)


@index_locked
def delete_by_doc_id(doc_id: str) -> int:
    """Delete all chunks belonging to a document. Returns count deleted."""
    collection = get_collection()
    # Get all chunks for this doc_id
    results = collection.get(
        where={"$and": [{"doc_id": doc_id}, current().filter]},
        include=[],
    )
    ids = results["ids"]
    if ids:
        collection.delete(ids=ids)
    return len(ids)


def production_filter():
    sources = eligible_sources()
    if not sources:
        return None
    allowed = [
        {"$and": [{"doc_id": doc_id}, {"file_hash": entry["file_hash"]}, {"version_id": entry["version_id"]}]}
        for doc_id, entry in sources.items()
    ]
    return {"$and": [
        current().filter, {"is_decoy": {"$ne": True}},
        ({"workspace_id": current().workspace_id} if current().personal else {"approved": True}),
        {"is_synthetic": {"$ne": True}},
        allowed[0] if len(allowed) == 1 else {"$or": allowed},
    ]}


@index_locked
def has_chunks(production=True):
    where = production_filter() if production else current().filter
    if production and where is None:
        return False
    kwargs = {"where": where} if where else {}
    return bool(get_collection().get(limit=1, include=[], **kwargs)["ids"])


@index_locked
def valid_cached_citations(citations):
    where = production_filter()
    if not where or not citations:
        return False
    records = get_collection().get(ids=citations, where=where, include=[])
    return set(records["ids"]) == set(citations)


@index_locked
def citation_fingerprint(citations):
    """Bind a cached answer to the exact approved content it cited."""
    where = production_filter()
    if not where or not citations:
        return None
    records = get_collection().get(ids=citations, where=where, include=["metadatas", "documents"])
    if set(records["ids"]) != set(citations):
        return None
    import hashlib
    parts = sorted((cid, m.get("file_hash"), hashlib.sha256(text.encode()).hexdigest())
                   for cid, m, text in zip(records["ids"], records["metadatas"], records["documents"]))
    return parts


@index_locked
def sync_authority_metadata():
    """Approval changes update flags without embedding unchanged files again."""
    collection = get_collection()
    records = collection.get(where=current().filter, include=["metadatas"])
    sources = eligible_sources()
    for cid, meta in zip(records["ids"], records["metadatas"]):
        entry = sources.get(meta.get("doc_id"))
        approved = bool(not current().personal and entry and meta.get("file_hash") == entry["file_hash"]
                        and not meta.get("is_decoy") and not meta.get("is_synthetic"))
        if meta.get("approved", False) != approved:
            collection.update(ids=[cid], metadatas=[{**meta, "approved": approved}])


@index_locked
def query(embedding: list[float], top_k: int | None = None,
          where: dict | None = None,
          production: bool = True) -> list[RetrievedChunk]:
    """
    Query the vector DB. Returns chunks sorted by similarity (descending).

    Args:
        embedding: Query embedding vector.
        top_k: Number of results (default from config).
        where: Optional extra metadata filter (merged with production filter).
        production: If True (default), exclude decoys and unapproved documents.

    Returns:
        List of RetrievedChunk with normalized similarity scores.
    """
    current()
    collection = get_collection()
    k = TOP_K if top_k is None else top_k
    if k < 1:
        raise ValueError("top_k must be positive")

    # Handle case where collection is empty or has fewer than k items
    count = collection.count()
    if count == 0:
        return []
    k = min(k, count)

    # Build production filter: exclude decoys and unapproved docs
    if production:
        prod_filter = production_filter()
        if prod_filter is None:
            return []
        if where:
            # Merge caller's filter into the $and list
            prod_filter["$and"].append(where)
        effective_where = prod_filter
    else:
        tenant = current().filter
        effective_where = {"$and": [tenant, where]} if where else tenant

    kwargs = {
        "query_embeddings": [embedding],
        "n_results": k,
        "include": ["documents", "metadatas", "distances"],
    }
    if effective_where:
        kwargs["where"] = effective_where

    results = collection.query(**kwargs)

    chunks: list[RetrievedChunk] = []
    if not results["ids"] or not results["ids"][0]:
        return chunks

    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        distance = results["distances"][0][i]

        chunks.append(RetrievedChunk(
            workspace_id=meta.get("workspace_id", ""),
            institution_id=meta.get("institution_id", ""),
            version_id=meta.get("version_id", ""),
            chunk_id=results["ids"][0][i],
            text=results["documents"][0][i],
            doc_id=meta.get("doc_id", ""),
            doc_title=meta.get("doc_title", ""),
            section=meta.get("section", ""),
            page=int(meta.get("page", 0)),
            chunk_index=int(meta.get("chunk_index", 0)),
            similarity=normalize_score(distance),
            is_decoy=bool(meta.get("is_decoy", False)),
            approved=bool(meta.get("approved", False)),
            is_synthetic=bool(meta.get("is_synthetic", False)),
            extraction_method=meta.get("extraction_method", "unknown"),
        ))

    return chunks


def get_collection_count() -> int:
    """Return the number of chunks in the collection."""
    return len(get_collection().get(where=current().filter, include=[])["ids"])


def reset_collection():
    """Refuse a shared-collection reset; remove explicit scoped documents instead."""
    raise ValueError('Shared collection reset is disabled')
