"""
retrieve.py — Retrieval module supporting raw, HyDE, and fusion modes.

Implements the retrieval step of the pipeline. Each mode returns
the same RetrievalResult structure for downstream consistency.
"""

import time
import asyncio
import copy
from dataclasses import dataclass, field
from typing import Optional

from src.embeddings import embed_single
from src.hyde import generate_hyde
from src.store import query as vector_query, RetrievedChunk, has_chunks
from src.config import TOP_K
from src.institutions import current


@dataclass
class RetrievalResult:
    """Result of a retrieval operation."""
    chunks: list[RetrievedChunk] = field(default_factory=list)
    hyde_text: Optional[str] = None
    hyde_failed: bool = False
    mode: str = "raw"
    timings_ms: dict = field(default_factory=dict)
    provider: Optional[str] = None
    llm_usage: dict = field(default_factory=dict)
    failovers: int = 0


async def retrieve_raw(question: str, top_k: int | None = None,
                       production: bool = True) -> RetrievalResult:
    """Baseline: embed the raw student question and search."""
    current()
    t0 = time.time()
    if not await asyncio.to_thread(has_chunks, production):
        return RetrievalResult(mode="raw", timings_ms={"total": round((time.time() - t0) * 1000, 1)})

    t_embed = time.time()
    q_embedding = await asyncio.to_thread(embed_single, question)
    embed_ms = (time.time() - t_embed) * 1000

    t_search = time.time()
    chunks = await asyncio.to_thread(vector_query, q_embedding, top_k=top_k or TOP_K, production=production)
    search_ms = (time.time() - t_search) * 1000

    return RetrievalResult(
        chunks=chunks,
        mode="raw",
        timings_ms={
            "embed": round(embed_ms, 1),
            "retrieve": round(search_ms, 1),
            "total": round((time.time() - t0) * 1000, 1),
        },
    )


async def retrieve_hyde(question: str, top_k: int | None = None,
                        production: bool = True) -> RetrievalResult:
    """HyDE: generate a synthetic passage, embed it, and search."""
    current()
    t0 = time.time()

    if not await asyncio.to_thread(has_chunks, production):
        return RetrievalResult(mode="hyde", timings_ms={"total": round((time.time() - t0) * 1000, 1)})

    # Generate HyDE text
    t_hyde = time.time()
    try:
        hyde_text, llm_resp = await generate_hyde(question)
        hyde_ms = (time.time() - t_hyde) * 1000
        provider = llm_resp.provider
    except Exception as e:
        print(f"  [retrieve] HyDE generation failed: {type(e).__name__}")
        # Fall back to raw retrieval
        result = await retrieve_raw(question, top_k, production=production)
        result.hyde_failed = True
        result.mode = "hyde"  # still report as hyde mode for tracing
        result.timings_ms["hyde"] = round((time.time() - t_hyde) * 1000 - result.timings_ms.get("total", 0), 1)
        result.timings_ms["total"] = round((time.time() - t0) * 1000, 1)
        return result

    if not hyde_text or len(hyde_text.strip()) < 10:
        print(f"  [retrieve] HyDE returned empty/short text, falling back to raw")
        result = await retrieve_raw(question, top_k, production=production)
        result.hyde_failed = True
        result.hyde_text = hyde_text
        result.mode = "hyde"
        result.timings_ms["total"] = round((time.time() - t0) * 1000, 1)
        return result

    # Embed the HyDE text
    t_embed = time.time()
    hyde_embedding = await asyncio.to_thread(embed_single, hyde_text)
    embed_ms = (time.time() - t_embed) * 1000

    # Search with HyDE embedding
    t_search = time.time()
    chunks = await asyncio.to_thread(vector_query, hyde_embedding, top_k=top_k or TOP_K, production=production)
    search_ms = (time.time() - t_search) * 1000

    return RetrievalResult(
        chunks=chunks,
        hyde_text=hyde_text,
        mode="hyde",
        timings_ms={
            "hyde": round(hyde_ms, 1),
            "embed": round(embed_ms, 1),
            "retrieve": round(search_ms, 1),
            "total": round((time.time() - t0) * 1000, 1),
        },
        provider=provider,
        failovers=getattr(llm_resp, "failovers", 0) if "llm_resp" in locals() and llm_resp else 0,
        llm_usage={"hyde": {"provider": provider, "model": getattr(llm_resp, "model", None),
                            "latency_ms": getattr(llm_resp, "latency_ms", None),
                            "input_tokens": getattr(llm_resp, "input_tokens", None),
                            "output_tokens": getattr(llm_resp, "output_tokens", None),
                            "cache_hit": getattr(llm_resp, "cached", False)}},
    )


async def retrieve_fusion(question: str, top_k: int | None = None,
                          production: bool = True) -> RetrievalResult:
    """
    Fusion: combine raw and HyDE retrieval using Reciprocal Rank Fusion (RRF).

    RRF_score(chunk) = sum(1 / (k + rank_i)) for each retrieval list i
    with k=60 (standard constant).

    IMPORTANT: The original cosine similarity is preserved on each chunk.
    The RRF score is stored separately in chunk.rrf_score and used only
    for ranking, NOT for the confidence gate.
    """
    current()
    t0 = time.time()
    k = top_k or TOP_K

    # Run both retrievals
    raw_result = await retrieve_raw(question, top_k=k + 3, production=production)
    hyde_result = await retrieve_hyde(question, top_k=k + 3, production=production)

    # RRF fusion
    rrf_scores: dict[str, float] = {}
    chunk_map: dict[str, RetrievedChunk] = {}
    best_similarity: dict[str, float] = {}  # track best cosine sim per chunk
    RRF_K = 60

    for rank, chunk in enumerate(raw_result.chunks):
        rrf_scores[chunk.chunk_id] = rrf_scores.get(chunk.chunk_id, 0) + 1.0 / (RRF_K + rank + 1)
        chunk_map[chunk.chunk_id] = chunk
        best_similarity[chunk.chunk_id] = max(
            best_similarity.get(chunk.chunk_id, 0.0), chunk.similarity
        )

    # A raw fallback is not an independent vote in reciprocal-rank fusion.
    for rank, chunk in enumerate([] if hyde_result.hyde_failed else hyde_result.chunks):
        rrf_scores[chunk.chunk_id] = rrf_scores.get(chunk.chunk_id, 0) + 1.0 / (RRF_K + rank + 1)
        if chunk.chunk_id not in chunk_map:
            chunk_map[chunk.chunk_id] = chunk
        best_similarity[chunk.chunk_id] = max(
            best_similarity.get(chunk.chunk_id, 0.0), chunk.similarity
        )

    # Sort by RRF score descending, take top_k
    sorted_ids = sorted(rrf_scores, key=lambda x: rrf_scores[x], reverse=True)[:k]

    fused_chunks = []
    for cid in sorted_ids:
        chunk = copy.copy(chunk_map[cid])
        # Preserve the best cosine similarity for confidence gating
        chunk.similarity = best_similarity[cid]
        # Store RRF score separately — never used as confidence
        chunk.rrf_score = rrf_scores[cid]
        fused_chunks.append(chunk)

    total_ms = (time.time() - t0) * 1000
    timings = {
        "raw": raw_result.timings_ms.get("total", 0),
        "hyde": hyde_result.timings_ms.get("total", 0),
        "total": round(total_ms, 1),
    }

    return RetrievalResult(
        chunks=fused_chunks,
        hyde_text=hyde_result.hyde_text,
        hyde_failed=hyde_result.hyde_failed,
        mode="fusion",
        timings_ms=timings,
        provider=hyde_result.provider,
        failovers=getattr(hyde_result, "failovers", 0),
        llm_usage=hyde_result.llm_usage,
    )


async def retrieve(question: str, mode: str = "hyde",
                   top_k: int | None = None,
                   production: bool = True) -> RetrievalResult:
    """
    Dispatch retrieval by mode.

    Args:
        question: Student's question.
        mode: "raw", "hyde", or "fusion".
        top_k: Override default TOP_K.
        production: If True, exclude decoys and unapproved docs.
    """
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question is required")
    if top_k is not None and top_k < 1:
        raise ValueError("top_k must be positive")
    dispatchers = {
        "raw": retrieve_raw,
        "hyde": retrieve_hyde,
        "fusion": retrieve_fusion,
    }
    from src.query_intent import search_question
    question = search_question(question)
    fn = dispatchers.get(mode)
    if fn is None:
        raise ValueError(f"Unknown retrieval mode: {mode}. Use: {list(dispatchers.keys())}")
    return await fn(question, top_k, production=production)

