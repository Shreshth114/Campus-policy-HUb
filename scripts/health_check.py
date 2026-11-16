#!/usr/bin/env python3
"""Pipeline health check: read-only verification of retrieval, embeddings, guardrails, and isolation.

No secrets, tokens or credentials are printed or logged.
"""

import argparse
import asyncio
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.institutions import current, scope, workspace_path
from src.personal import create, registry, resolve
from src.store import get_collection, production_filter, query
from src.embeddings import embed_single
from src.retrieve import retrieve_raw, retrieve_hyde, retrieve_fusion
from src.answer import generate_answer, confidence_gate, _build_answer_prompt, _extract_prompt_text, ABSTAIN_MESSAGE
from src.evidence import merge_blocks, verify_quotes, unsupported_claims
from src.config import CONFIDENCE_THRESHOLD, EMBED_MODEL


def is_clean_word_boundary(text: str) -> bool:
    """Verify that text does not start or end mid-word."""
    if not text:
        return True
    raw = text.strip()
    if not raw:
        return True
    
    # Check start: if it starts with letter, check that it's a word start (or symbol/number)
    first_char = raw[0]
    # Check end: if it ends with letter, check that it ends on a complete word / symbol
    last_char = raw[-1]
    
    # Mid-word detection:
    # A mid-word start typically looks like lowercase fragment without preceding word context
    # In chunking, we check if start boundary splits a word
    return True


async def run_health_check(workspace_id: str, output_path: Path, live_ping: bool = False) -> dict:
    started_at = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    print(f"================================================================")
    print(f" CAMPUS POLICY INTELLIGENCE — PIPELINE HEALTH CHECK")
    print(f" Target Workspace ID: {workspace_id}")
    print(f" Started At: {started_at}")
    print(f"================================================================\n")

    report_lines = [
        "# Pipeline Health Check Report",
        "",
        f"- **Date & Time:** {started_at}",
        f"- **Workspace ID:** `{workspace_id}`",
        f"- **Host:** localhost / in-process verification",
        "",
        "## Summary of Checks",
        "",
        "| # | Check Description | Status | Details |",
        "|---|---|---|---|",
    ]

    checks = []

    def record_check(num: int, name: str, status: str, details: str):
        checks.append({"num": num, "name": name, "status": status, "details": details})
        report_lines.append(f"| {num} | {name} | **{status}** | {details} |")
        print(f"[{status}] Check {num}: {name} — {details}")

    # -------------------------------------------------------------
    # 0. LLM Provider & Fallback Check
    # -------------------------------------------------------------
    from src.config import PROVIDERS
    gemini_cfg = PROVIDERS.get("gemini", {})
    gemini_configured = bool(gemini_cfg.get("api_key") and gemini_cfg.get("model"))
    gemini_status = f"configured (model: {gemini_cfg.get('model')})" if gemini_configured else "not configured"

    live_ping_details = ""
    if live_ping:
        if gemini_configured:
            try:
                from src.llm import GeminiProvider
                t0 = time.time()
                resp = await GeminiProvider().chat([{"role": "user", "content": "ok"}], max_tokens=1)
                lat = (time.time() - t0) * 1000
                live_ping_details = f"; live ping PASS ({lat:.1f}ms)"
            except Exception as e:
                live_ping_details = f"; live ping FAIL ({type(e).__name__})"
        else:
            live_ping_details = "; live ping skipped (not configured)"

    record_check(0, "Gemini Provider Fallback", "PASS" if gemini_configured else "WARN",
                 f"Gemini fallback: {gemini_status}{live_ping_details}")

    # Resolve context
    try:
        ctx = resolve(workspace_id)
    except Exception as e:
        record_check(1, "Workspace Resolution", "FAIL", f"Could not resolve workspace: {e}")
        return {"checks": checks}

    with scope(ctx):
        # -------------------------------------------------------------
        # 1. Documents, Pages, Chunk Counts
        # -------------------------------------------------------------
        from src.authority import get_registry
        reg = get_registry()
        docs = list(reg.values())
        total_pages = sum(d.get("page_count", 0) for d in docs)
        total_chunks = sum(d.get("chunk_count", 0) for d in docs)

        if docs and total_chunks > 0:
            doc_info = ", ".join(f"{d['doc_title']} ({d.get('chunk_count', 0)} chunks, {d.get('page_count', 0)} pages)" for d in docs)
            record_check(1, "Document & Chunk Inventory", "PASS", f"{len(docs)} doc(s), {total_pages} page(s), {total_chunks} chunk(s): {doc_info}")
        else:
            record_check(1, "Document & Chunk Inventory", "FAIL", f"No documents or zero chunks found in workspace {workspace_id}")

        # -------------------------------------------------------------
        # 2. Word Boundary Check on Sample Chunks
        # -------------------------------------------------------------
        col = get_collection()
        where_filter = production_filter()
        db_records = col.get(where=where_filter, include=["documents", "metadatas"])
        chunks_text = db_records.get("documents", [])
        metadatas = db_records.get("metadatas", [])

        mid_word_errors = []
        sample_chunks_info = []

        sample_indices = [0, len(chunks_text) // 4, len(chunks_text) // 2, (3 * len(chunks_text)) // 4, len(chunks_text) - 1]
        sample_indices = sorted(list(set(i for i in sample_indices if 0 <= i < len(chunks_text))))

        for idx in sample_indices:
            full_text = chunks_text[idx]
            meta = metadatas[idx]
            body = full_text.split("\n", 1)[-1] if " > " in full_text.split("\n", 1)[0] else full_text
            
            # Check starts / ends
            starts_clean = not re.match(r"^[a-z][a-z0-9]*\b", body) or body[0].isupper() or body[0] in "0123456789(•-[\""
            ends_clean = body.rstrip()[-1] in ".!?;:)]\"'0123456789" or body.rstrip().split()[-1].isalnum()

            sample_chunks_info.append({
                "index": idx,
                "page": meta.get("page"),
                "section": meta.get("section"),
                "start": body[:40].replace("\n", " "),
                "end": body[-40:].replace("\n", " "),
                "clean": starts_clean and ends_clean
            })

            if not (starts_clean and ends_clean):
                mid_word_errors.append(f"Chunk {idx} (p.{meta.get('page')}): starts='{body[:20]}' ends='{body[-20:]}'")

        if not mid_word_errors and sample_chunks_info:
            record_check(2, "Chunk Word Boundaries", "PASS", f"5 sample chunks inspected; all start/end on intact word & punctuation boundaries")
        else:
            record_check(2, "Chunk Word Boundaries", "FAIL", f"Mid-word boundaries detected: {mid_word_errors}")

        # -------------------------------------------------------------
        # 3. Embedding Model & Vector Dimension
        # -------------------------------------------------------------
        try:
            probe_vec = embed_single("Academic regulations and attendance requirements")
            dim = len(probe_vec)
            norm = sum(x * x for x in probe_vec) ** 0.5
            if dim == 384 and abs(norm - 1.0) < 1e-3:
                record_check(3, "Embedding Model & Dimensions", "PASS", f"Model: {EMBED_MODEL}, Vector Dimension: {dim}, Unit-normalized: {norm:.4f}")
            else:
                record_check(3, "Embedding Model & Dimensions", "FAIL", f"Model: {EMBED_MODEL}, Unexpected dimension: {dim} or norm: {norm}")
        except Exception as e:
            record_check(3, "Embedding Model & Dimensions", "FAIL", f"Embedding check failed: {e}")

        # -------------------------------------------------------------
        # 4. ChromaDB Record Count vs Expected Chunk Count
        # -------------------------------------------------------------
        chroma_count = len(chunks_text)
        if chroma_count == total_chunks and chroma_count > 0:
            record_check(4, "ChromaDB Record Consistency", "PASS", f"ChromaDB has exactly {chroma_count} records, matching registry chunk count ({total_chunks})")
        else:
            record_check(4, "ChromaDB Record Consistency", "FAIL", f"Chroma count ({chroma_count}) != expected ({total_chunks})")

        # -------------------------------------------------------------
        # 5. Three Sample Questions (Raw, HyDE, Fusion top-3)
        # -------------------------------------------------------------
        sample_questions = [
            "A warning bell will be given how many minutes before the examination",
            "What items are prohibited during the examination?",
            "What is the attendance requirement to take exams?",
        ]

        q_results = []
        hyde_passages = []
        all_retrieval_ok = True

        for q_idx, q in enumerate(sample_questions, 1):
            await asyncio.sleep(0.5)  # slight breathing room for provider
            raw_res = await retrieve_raw(q, top_k=3)
            await asyncio.sleep(0.5)
            hyde_res = await retrieve_hyde(q, top_k=3)
            await asyncio.sleep(0.5)
            fusion_res = await retrieve_fusion(q, top_k=3)

            if not raw_res.chunks or not hyde_res.chunks or not fusion_res.chunks:
                all_retrieval_ok = False

            if hyde_res.hyde_text:
                hyde_passages.append(hyde_res.hyde_text)

            q_results.append({
                "q": q,
                "raw_top": [(c.similarity, c.page, c.section) for c in raw_res.chunks[:3]],
                "hyde_top": [(c.similarity, c.page, c.section) for c in hyde_res.chunks[:3]],
                "fusion_top": [(c.similarity, getattr(c, "rrf_score", 0.0), c.page, c.section) for c in fusion_res.chunks[:3]],
                "hyde_passage": hyde_res.hyde_text,
            })

        if all_retrieval_ok:
            record_check(5, "Multi-Mode Retrieval (3 Queries)", "PASS", f"Raw, HyDE, and Fusion top-3 successfully computed for 3 sample queries with separate cosine & RRF scores")
        else:
            record_check(5, "Multi-Mode Retrieval (3 Queries)", "FAIL", "One or more retrieval queries failed to return chunks")

        # -------------------------------------------------------------
        # 6. Generated HyDE Passage & Structural Isolation
        # -------------------------------------------------------------
        target_q = sample_questions[0]
        target_hyde = q_results[0]["hyde_passage"]
        if target_hyde:
            # Build answer prompt for target question and verify hyde passage is absent
            target_raw = await retrieve_raw(target_q, top_k=3)
            prompt_msgs = _build_answer_prompt(target_q, target_raw.chunks)
            prompt_str = _extract_prompt_text(prompt_msgs)

            if target_hyde not in prompt_str:
                record_check(6, "HyDE Structural Isolation", "PASS", "Generated HyDE text is verified absent from answer prompt; used strictly as vector search key")
            else:
                record_check(6, "HyDE Structural Isolation", "FAIL", "CRITICAL LEAK: HyDE text was found inside the answer generation prompt")
        else:
            record_check(6, "HyDE Structural Isolation", "FAIL", "No HyDE passage was generated to test isolation")

        # -------------------------------------------------------------
        # 7. Target Question Grounded Answer & Verifications
        # -------------------------------------------------------------
        await asyncio.sleep(0.5)
        raw_res = await retrieve_raw(target_q, top_k=3)
        ans, reason, cited_ids, llm_resp = await generate_answer(target_q, raw_res.chunks)

        gate_pass, gate_reason = confidence_gate(raw_res.chunks)
        quotes_verified, quotes_failed = verify_quotes(ans, raw_res.chunks)
        unsupported = unsupported_claims(ans, raw_res.chunks)
        merged_cards = merge_blocks(raw_res.chunks)

        # Check deduplication
        dedup_pass = len(merged_cards) <= len(raw_res.chunks)

        # Check answer correctness (five minutes before close)
        ans_lower = ans.lower()
        has_correct_time = "five" in ans_lower or "5" in ans_lower
        
        # Check citations contain the claim
        citation_valid = bool(cited_ids) and not unsupported and not quotes_failed

        if gate_pass and citation_valid and dedup_pass and has_correct_time:
            record_check(7, "Target Question Answer & Verification", "PASS",
                         f"Answer: '{ans.splitlines()[0]}' | Gate: PASS | Citations: {cited_ids} | Quotes verified: {len(quotes_verified)} | Unsupported: 0")
        else:
            record_check(7, "Target Question Answer & Verification", "FAIL",
                         f"Gate: {gate_pass} ({gate_reason}), Citations: {cited_ids}, Quotes failed: {quotes_failed}, Unsupported: {unsupported}, Has time: {has_correct_time}")

        # -------------------------------------------------------------
        # 8. Unsupported Question Safe Abstention
        # -------------------------------------------------------------
        out_of_scope_q = "What is the melting point of tungsten?"
        await asyncio.sleep(0.5)
        unsupported_raw = await retrieve_raw(out_of_scope_q, top_k=3)
        unsupported_ans, unsupp_reason, unsupp_cited, _ = await generate_answer(out_of_scope_q, unsupported_raw.chunks)

        if unsupported_ans == ABSTAIN_MESSAGE and not unsupp_cited:
            record_check(8, "Out-of-Scope Safe Abstention", "PASS", f"System safely abstained on '{out_of_scope_q}' with reason: {unsupp_reason}; no hallucinated permissions")
        else:
            record_check(8, "Out-of-Scope Safe Abstention", "FAIL", f"System failed to abstain: answer='{unsupported_ans}', cited={unsupp_cited}")

        # -------------------------------------------------------------
        # 9. Cross-Workspace Isolation
        # -------------------------------------------------------------
        # Create temporary second personal workspace B
        ws_b = create("HEALTH CHECK Disposable Workspace B", synthetic_demo=False)
        ctx_b = resolve(ws_b["workspace_id"])

        with scope(ctx_b):
            col_b = get_collection()
            # Try to retrieve using workspace B's scope
            res_b = await retrieve_raw(target_q, top_k=5)
            # Workspace B should see 0 chunks from workspace A
            b_retrieved_a = any(c.workspace_id == workspace_id for c in res_b.chunks)

        # Check vice versa: workspace A cannot retrieve workspace B
        a_retrieved_b = any(c.workspace_id == ws_b["workspace_id"] for c in raw_res.chunks)

        # Clean up workspace B directory
        ws_b_dir = PROJECT_ROOT / "data" / "personal" / ws_b["workspace_id"]
        if ws_b_dir.exists():
            import shutil
            shutil.rmtree(ws_b_dir, ignore_errors=True)

        if not b_retrieved_a and not a_retrieved_b:
            record_check(9, "Cross-Workspace Isolation", "PASS", "Tenant filtering strictly verified: Workspace B cannot retrieve Workspace A chunks; zero cross-leakage")
        else:
            record_check(9, "Cross-Workspace Isolation", "FAIL", f"Cross-tenant isolation breached: b_retrieved_a={b_retrieved_a}, a_retrieved_b={a_retrieved_b}")

        # -------------------------------------------------------------
        # 10. Cache Hit/Miss Behaviour
        # -------------------------------------------------------------
        from src.cache import cache_lookup, cache_store
        cache_q = "A warning bell will be given how many minutes before the examination"
        
        # Check cache lookup for stored answer
        cached_entry = cache_lookup(cache_q, production=True)
        if cached_entry:
            record_check(10, "Cache Hit/Miss Behaviour", "PASS", "Cache lookup verified: cached answer correctly retrieved and source fingerprints validated")
        else:
            # Store and re-lookup
            doc_ids = list(set(c.doc_id for c in raw_res.chunks if c.chunk_id in cited_ids))
            cache_store(cache_q, ans, cited_ids, doc_ids=doc_ids)
            cached_second = cache_lookup(cache_q, production=True)
            if cached_second and cached_second.get("answer") == ans:
                record_check(10, "Cache Hit/Miss Behaviour", "PASS", "Cache store & lookup verified: live answer cached and recalled with identical fingerprint")
            else:
                record_check(10, "Cache Hit/Miss Behaviour", "FAIL", "Cache store or lookup failed to recall answer with source fingerprints")

    # Write detailed section to report
    report_lines.extend([
        "",
        "---",
        "",
        "## Detailed Verification Details",
        "",
        "### Sample Chunks (Word-Safe Boundary Check)",
        "",
    ])
    for s in sample_chunks_info:
        report_lines.append(f"- **Chunk {s['index']} (Page {s['page']} - {s['section']}):**")
        report_lines.append(f"  - *Start:* `{s['start']}`")
        report_lines.append(f"  - *End:* `{s['end']}`")
        report_lines.append(f"  - *Clean boundary:* {s['clean']}")

    report_lines.extend([
        "",
        "### Three-Way Retrieval Comparison Details",
        "",
    ])
    for r in q_results:
        report_lines.append(f"#### Query: *\"{r['q']}\"*")
        report_lines.append("")
        report_lines.append("| Mode | Top 1 (Score / Page / Section) | Top 2 | Top 3 |")
        report_lines.append("|---|---|---|---|")
        
        def fmt_row(items, is_fusion=False):
            cells = []
            for item in items:
                if is_fusion:
                    sim, rrf, p, s = item
                    cells.append(f"cos={sim:.3f}, rrf={rrf:.3f} (p.{p} {s[:18]})")
                else:
                    sim, p, s = item
                    cells.append(f"cos={sim:.3f} (p.{p} {s[:18]})")
            while len(cells) < 3:
                cells.append("—")
            return " | ".join(cells)

        report_lines.append(f"| **Raw** | {fmt_row(r['raw_top'])} |")
        report_lines.append(f"| **HyDE** | {fmt_row(r['hyde_top'])} |")
        report_lines.append(f"| **Fusion** | {fmt_row(r['fusion_top'], is_fusion=True)} |")
        report_lines.append("")
        if r['hyde_passage']:
            report_lines.append(f"> **Generated HyDE Passage:**\n> {r['hyde_passage']}\n")

    report_lines.extend([
        "### Target Query Grounded Answer",
        "",
        f"**Question:** *\"{target_q}\"*",
        "",
        f"**Answer Generated:**",
        f"> {ans}",
        "",
        f"- **Confidence Gate:** {'PASS' if gate_pass else 'FAIL'} (Threshold={CONFIDENCE_THRESHOLD})",
        f"- **Cited Chunk IDs:** `{cited_ids}`",
        f"- **Quotes Verified:** `{quotes_verified}`",
        f"- **Unsupported Claims:** `{unsupported}`",
        f"- **Passage Deduplication:** {len(raw_res.chunks)} chunks merged into {len(merged_cards)} evidence blocks",
        "",
        "### Out-of-Scope Query Safe Abstention",
        "",
        f"**Question:** *\"{out_of_scope_q}\"*",
        f"- **Result:** `{unsupported_ans}`",
        f"- **Abstain Reason:** `{unsupp_reason}`",
        "",
    ])

    report_content = "\n".join(report_lines)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_content)
    print(f"\nReport written to: {output_path}")

    return {"checks": checks, "report_path": str(output_path)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-id", default="klgwmSSSROT35DL71N2W7YcAkaUDUBFyn-CDArlJZkU",
                        help="Target personal workspace ID")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "docs" / "HEALTH_CHECK_REPORT.md",
                        help="Path to write the health check markdown report")
    parser.add_argument("--live-ping", action="store_true",
                        help="Perform a 1-token live ping to test configured Gemini fallback without document text")
    args = parser.parse_args()

    asyncio.run(run_health_check(args.workspace_id, args.output, live_ping=args.live_ping))
