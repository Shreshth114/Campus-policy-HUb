"""
pipeline.py — Main pipeline: ask(question, mode) -> Trace.

Orchestrates: cache → HyDE → retrieval → confidence gate → answer → citation check → cache store.
"""

import time
import asyncio

from src.trace import Trace, ChunkTrace
from src.institutions import current
from src.retrieve import retrieve, RetrievalResult
from src.answer import generate_answer, ABSTAIN_MESSAGE
from src.cache import cache_lookup, cache_store
from src.store import valid_cached_citations
from src.evidence import ids as evidence_ids,merge_blocks,connect_continuations,relevant_sentence,verify_quotes
from src.answer import confidence_gate, validate_answer
from src.llm import ProviderUnavailableError


async def ask(question: str, mode: str = "hyde",
              use_cache: bool = True) -> Trace:
    """
    Full pipeline: question → trace.

    Args:
        question: Student's casual question.
        mode: Retrieval mode — "raw", "hyde", or "fusion".
        use_cache: Whether to check/store in semantic cache.

    Returns:
        Trace with all intermediate results and timings.
    """
    if not isinstance(question, str):
        raise ValueError("Question must be text")
    question = question.strip()
    if not question or len(question) > 500:
        raise ValueError("Question must contain 1–500 characters")
    if mode not in {"raw", "hyde", "fusion"}:
        raise ValueError("Unknown retrieval mode")
    t_total = time.time()
    trace = Trace(question=question, mode=mode, institution_id=current().institution_id,workspace_id=current().workspace_id,
                  trust_level='personal_unverified' if current().personal else 'institutional',
                  trust_notice=__import__('src.personal',fromlist=['TRUST_NOTICE']).TRUST_NOTICE if current().personal else '')

    if current().personal:trace.synthetic_demo=__import__('src.personal',fromlist=['registry']).registry().get(current().workspace_id,{}).get('synthetic_demo',False)

    from src.question_coverage import question_requirements
    trace.question_requirements=question_requirements(question)
    from src.query_intent import understand
    clarification = understand(question)['clarification']
    if clarification:
        trace.decision = 'clarification_required'
        trace.answer = clarification
        return trace

    # ── Step 1: Cache lookup ───────────────────────────────────
    t_cache = time.time()
    if use_cache:
        try:
            cached = await asyncio.to_thread(cache_lookup, question)
            cached_chunks = [ChunkTrace(**c) for c in cached.get("retrieved", [])] if cached else []
        except Exception:
            cached = None
            trace.warnings.append("Answer cache unavailable; running a fresh search")
        if cached is not None and (any(not current().owns(c) for c in cached_chunks)
                                    or not await asyncio.to_thread(valid_cached_citations, [cid for c in cached_chunks for cid in (c.source_chunk_ids or [c.chunk_id])])
                                    or not await asyncio.to_thread(valid_cached_citations, cached.get('citations',[]))):
            cached=None
        if cached is not None:
            # Legacy cache entries do not record the exact sent excerpts: miss safely.
            import copy
            from src.config import ANSWER_CHUNKS_LIMIT
            sent = [copy.copy(c) for c in cached_chunks if c.answer_excerpt is not None][:ANSWER_CHUNKS_LIMIT]
            if not sent or any(not c.answer_excerpt for c in sent):
                cached = None
            else:
                for c in sent:
                    c.text = c.answer_excerpt
                reason, checked_ids, failures = validate_answer(cached['answer'], sent)
                from src.grounding import proof_matches
                if not reason and not proof_matches(cached.get('grounding_proof'),question,cached['answer'],sent):
                    reason = 'cached_grounding_review_missing_or_stale'
                    failures.append({'reason':reason})
                if not reason and set(checked_ids) != set(cached.get('citations', [])):
                    reason = 'citation_check_failed'
                    failures.append({'reason':'cached_citation_mapping_mismatch'})
                from src.answer_diagnostics import record_answer
                from src.answer import _build_answer_prompt
                record_answer(_build_answer_prompt(question, sent, trim=False), cached_chunks[:len(sent)],
                              sent, cached['answer'], reason, failures)
                if reason:
                    cached = None
                else:
                    verified, _ = verify_quotes(cached['answer'], sent)
        if cached is not None:
            trace.evidence_coverage=cached['grounding_proof']['review']['coverage']
            trace.verified_quotes=verified;trace.citations_verified=True;trace.confidence_passed=True
            trace.cache_hit = True
            trace.cache_similarity = cached.get("similarity", 1.0)
            trace.answer = __import__('src.answer',fromlist=['canonicalize_citations']).canonicalize_citations(cached["answer"])
            trace.citations = cached.get("citations", [])
            trace.retrieved = cached_chunks
            trace.decision = "answered"
            trace.timings_ms["cache"] = round((time.time() - t_cache) * 1000, 1)
            trace.timings_ms["total"] = round((time.time() - t_total) * 1000, 1)
            return trace
    trace.timings_ms["cache"] = round((time.time() - t_cache) * 1000, 1)

    # ── Step 2: Retrieve ───────────────────────────────────────
    try:
        retrieval: RetrievalResult = await retrieve(question, mode=mode, production=True)
    except Exception:
        trace.error = "Retrieval failed; check the local server logs."
        trace.decision = "abstained"
        trace.abstain_reason = "retrieval_error"
        trace.answer = ABSTAIN_MESSAGE
        trace.timings_ms["total"] = round((time.time() - t_total) * 1000, 1)
        return trace

    retrieval.chunks=merge_blocks(connect_continuations(retrieval.chunks))
    trace.confidence_passed=confidence_gate(retrieval.chunks)[0]
    trace.hyde_text = retrieval.hyde_text
    trace.hyde_failed = retrieval.hyde_failed
    trace.provider = retrieval.provider
    trace.failovers = getattr(retrieval, "failovers", 0)
    trace.llm_usage.update(retrieval.llm_usage)

    # Merge retrieval timings
    for k, v in retrieval.timings_ms.items():
        trace.timings_ms[k] = v

    # Convert chunks to trace format
    trace.retrieved = [
        ChunkTrace(
            workspace_id=c.workspace_id,
            institution_id=c.institution_id,
            doc_id=c.doc_id,
            version_id=c.version_id,
            chunk_id=c.chunk_id,
            doc_title=c.doc_title,
            section=c.section,
            page=c.page,
            score=c.similarity,
            text_preview=relevant_sentence(c.text,question),
            matched_sentence=relevant_sentence(c.text,question),
            text=c.text,source_chunk_ids=c.source_chunk_ids or [c.chunk_id],pages=c.pages or [c.page],
            is_decoy=c.is_decoy,
            rrf_score=c.rrf_score,
            approved=c.approved,
            is_synthetic=c.is_synthetic,
            extraction_method=c.extraction_method,
        )
        for c in retrieval.chunks
    ]

    # ── Step 3: Generate answer ────────────────────────────────
    t_answer = time.time()
    try:
        answer_text, abstain_reason, cited_ids, llm_resp = await generate_answer(
            question=question,
            chunks=retrieval.chunks,
        )
    except ProviderUnavailableError as exc:
        rec_retry = int(exc.retry_after or 15)
        trace.decision = "provider_unavailable"
        trace.abstain_reason = None
        trace.retry_after_s = float(rec_retry)
        trace.provider = exc.provider or trace.provider
        msg = f"The AI provider is rate-limited. Retrying in {rec_retry} seconds"
        trace.error = msg
        trace.answer = msg
        trace.timings_ms["total"] = round((time.time() - t_total) * 1000, 1)
        return trace
    except Exception as exc:
        trace.decision = "abstained"
        trace.abstain_reason = "answer_error"
        trace.error = "Answer generation failed"
        trace.answer = ABSTAIN_MESSAGE
        trace.timings_ms["total"] = round((time.time() - t_total) * 1000, 1)
        return trace

    trace.timings_ms["answer"] = round((time.time() - t_answer) * 1000, 1)

    if llm_resp:
        trace.validation_failures = getattr(llm_resp,'validation_failures',[])
        trace.evidence_coverage = getattr(llm_resp,'evidence_coverage',[])
        excerpts = getattr(llm_resp, 'answer_excerpts', {})
        if isinstance(excerpts, dict):
            order = {cid:i for i,cid in enumerate(excerpts)}
            trace.retrieved.sort(key=lambda c: order.get(c.chunk_id,len(order)))
            for c in trace.retrieved:
                c.answer_excerpt = excerpts.get(c.chunk_id)
        if isinstance(getattr(llm_resp,'review_usage',None),dict):
            trace.llm_usage['answer_review'] = llm_resp.review_usage
        trace.provider = llm_resp.provider
        trace.failovers = getattr(llm_resp, "failovers", 0) or trace.failovers
        trace.tokens_estimated_before = getattr(llm_resp, "tokens_estimated_before", None)
        trace.tokens_estimated_after = getattr(llm_resp, "tokens_estimated_after", None)
        trace.llm_usage["answer"] = {
            "provider": llm_resp.provider, "model": llm_resp.model,
            "latency_ms": llm_resp.latency_ms, "input_tokens": llm_resp.input_tokens,
            "output_tokens": llm_resp.output_tokens,
            "finish_reason": getattr(llm_resp,"finish_reason",None),
            "reasoning_tokens": getattr(llm_resp,"reasoning_tokens",None),
            "tokens_estimated_before": getattr(llm_resp, "tokens_estimated_before", None),
            "tokens_estimated_after": getattr(llm_resp, "tokens_estimated_after", None),
        }

    if not abstain_reason:
        try:
            still_valid = await asyncio.to_thread(valid_cached_citations, evidence_ids([c for c in retrieval.chunks if c.chunk_id in cited_ids]))
        except Exception:
            still_valid = False
            trace.error = "Source validation is unavailable; retry when local storage is ready."
        if not still_valid:
            answer_text, abstain_reason, cited_ids = ABSTAIN_MESSAGE, (
                "source_validation_error" if trace.error else "source_changed"), []
    sent_order=getattr(llm_resp,'answer_excerpts',{}) if llm_resp else {}
    sent_for_quotes=[next(c for c in retrieval.chunks if c.chunk_id==cid) for cid in sent_order] if isinstance(sent_order,dict) and sent_order else retrieval.chunks
    trace.verified_quotes=verify_quotes(answer_text,sent_for_quotes)[0] if not abstain_reason else []
    if trace.verified_quotes:
        from src.evidence import sentences,quote_in_source
        for index,c in enumerate(trace.retrieved,1):
            quotes=[q['quote'] for q in trace.verified_quotes if 'C'+str(index) in q['labels']]
            matched=[s for s in sentences(c.text) if any(quote_in_source(q,s) for q in quotes)]
            if matched:c.matched_sentence=' '.join(dict.fromkeys(matched))
    trace.citations_verified=not bool(abstain_reason)
    if abstain_reason=="quote_verification_failed":trace.warnings.append("Quote could not be verified; the proposed answer was withheld.")
    trace.answer = answer_text
    trace.citations = cited_ids

    if abstain_reason:
        trace.decision = "abstained"
        trace.abstain_reason = abstain_reason
    else:
        trace.decision = "answered"

        # ── Step 4: Cache store ────────────────────────────────
        if use_cache:
            # Collect doc_ids from cited chunks
            doc_ids = list(set(
                c.doc_id for c in retrieval.chunks
                if c.chunk_id in cited_ids
            ))
            try:
                await asyncio.to_thread(cache_store,
                    question=question,
                    answer=answer_text,
                    citations=cited_ids,
                    doc_ids=doc_ids,
                    retrieved=trace.to_dict()["retrieved"],
                    grounding_proof=getattr(llm_resp,"grounding_proof",None) if llm_resp else None,
                )
            except Exception:
                trace.warnings.append("Answer could not be saved in the cache")

    trace.timings_ms["total"] = round((time.time() - t_total) * 1000, 1)
    return trace

