#!/usr/bin/env python3
"""Verified-label benchmark. Missing labels produce a blocked report, never fake zeros."""
import argparse
import asyncio
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import sys
import time
import re

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.retrieve import retrieve
from src.pipeline import ask
from src.config import CONFIDENCE_THRESHOLD
from src.hyde import cache_enabled
from src.persistence import write_json
from src.institutions import current, workspace_path, resolve, scope
from src.store import has_chunks, valid_cached_citations

BENCH_DIR = Path(__file__).parent
QUERIES_PATH = BENCH_DIR / "test_queries.jsonl"
RESULTS_DIR = BENCH_DIR / "results"
MODES = ("raw", "hyde", "fusion")


def load_queries():
    queries, ids = [], set()
    for line in workspace_path('queries').read_text().splitlines():
        if not line.strip():
            continue
        q = json.loads(line)
        if not isinstance(q, dict) or not isinstance(q.get("query"), str) or not q["query"].strip():
            raise ValueError("Every query needs nonempty text")
        if not isinstance(q.get("id"), str) or q["id"] in ids:
            raise ValueError("Every query needs a unique id")
        gold = q.get("gold_chunk_ids", [])
        if not isinstance(gold, list) or any(not isinstance(cid, str) or not cid for cid in gold):
            raise ValueError("gold_chunk_ids must be a list of chunk IDs")
        if not isinstance(q.get("labels_verified", False), bool):
            raise ValueError("labels_verified must be boolean")
        if (q.get('workspace_id')!=current().workspace_id if current().personal else q.get('institution_id')!=current().institution_id): raise ValueError("Foreign benchmark label")
        ids.add(q["id"])
        queries.append(q)
    return queries


def eligible(q, synthetic=False):
    if q.get("is_synthetic"):
        return synthetic and (bool(q.get("gold_chunk_ids")) or q.get("expect") == "abstain")
    return q.get("labels_verified") is True and (
        bool(q.get("gold_chunk_ids")) or q.get("expect") == "abstain")


def mean(values):
    return sum(values) / len(values) if values else None


def threshold_sweep(observations, thresholds=(0.2, 0.35, 0.5, 0.65)):
    """Retrieval proxy only; this does not measure semantic answer correctness."""
    rows = []
    for threshold in thresholds:
        accepted = [r for r in observations if r["best_similarity"] is not None
                    and r["best_similarity"] >= threshold and not r.get("error")]
        rows.append({"threshold": threshold, "retrieval_acceptance_rate": len(accepted) / len(observations)
                     if observations else None,
                     "accepted_without_gold_rate": mean([not r["gold_hit"] for r in accepted])})
    return rows


async def evaluate_retrieval(queries, mode, use_cache=True, slow=0, synthetic=False):
    token = cache_enabled.set(use_cache)
    observations = []
    recalls = {k: [] for k in (1, 3, 5)}
    hits = {k: [] for k in (1, 3, 5)}
    ranks, latencies = [], []
    stage_latencies={key:[] for key in ("hyde","embed","retrieve")}
    try:
        for q in queries:
            if not eligible(q, synthetic) or not q.get("gold_chunk_ids"):
                continue
            if slow:
                await asyncio.sleep(slow)
            gold = set(q["gold_chunk_ids"])
            row = {"id": q["id"], "query": q["query"], "gold_hit": False, "best_similarity": None, "error": None}
            try:
                result = await retrieve(q["query"], mode=mode, production=not synthetic)
                ids = [c.chunk_id for c in result.chunks]
                row.update(retrieved_ids=ids, gold_hit=bool(gold & set(ids)),
                           best_similarity=max((c.similarity for c in result.chunks), default=None),
                           hyde_failed=result.hyde_failed,
                           hyde_text=result.hyde_text, llm_usage=result.llm_usage,
                           decoy_retrieved=sum(c.is_decoy for c in result.chunks))
                latencies.append(result.timings_ms.get("total", 0))
                row['timings_ms']=result.timings_ms
                for key,values in stage_latencies.items():
                    if key in result.timings_ms:values.append(result.timings_ms[key])
            except Exception as exc:
                ids = []
                row["error"] = type(exc).__name__
            for k in recalls:
                overlap = len(gold & set(ids[:k]))
                recalls[k].append(overlap / len(gold))
                hits[k].append(float(overlap > 0))
            row['reciprocal_rank'] = next((1 / i for i, cid in enumerate(ids, 1) if cid in gold), 0)
            row['recall_at_3'] = len(gold & set(ids[:3])) / len(gold)
            ranks.append(row['reciprocal_rank'])
            observations.append(row)
    finally:
        cache_enabled.reset(token)
    return {**{f"recall_at_{k}": mean(v) for k, v in recalls.items()},
            **{f"hit_at_{k}": mean(v) for k, v in hits.items()},
            "mrr": mean(ranks), "mean_latency_ms": mean(latencies),
            **{f"mean_{key}_latency_ms":mean(values) for key,values in stage_latencies.items()},
            "n_queries": len(observations), "errors": sum(bool(r["error"]) for r in observations),
            "hyde_failures": sum(bool(r.get("hyde_failed")) for r in observations),
            "observations": observations, "threshold_sweep": threshold_sweep(observations)}


async def evaluate_safety(queries, mode, slow=0):
    oos, oos_correct, false_abstains, answered, valid, errors, decoys, unapproved = 0, 0, 0, 0, 0, 0, 0, 0
    answerable = 0
    uncited_sentences = 0
    clarifications = 0
    for q in queries:
        if not eligible(q) or q.get("is_synthetic"):
            continue
        if slow:
            await asyncio.sleep(slow)
        is_oos = q.get("expect") == "abstain"
        oos += int(is_oos)
        answerable += int(not is_oos)
        try:
            trace = await ask(q["query"], mode=mode, use_cache=False)
            if trace.decision == "provider_unavailable" or trace.error:
                errors += 1
                continue
            if trace.decision == 'clarification_required':
                clarifications += 1
                continue
            if trace.decision not in {'answered','abstained'}:
                errors += 1
                continue
            if trace.decision == "abstained":
                oos_correct += int(is_oos)
                false_abstains += int(not is_oos)
            else:
                answered += 1
                retrieved = {c.chunk_id: c for c in trace.retrieved}
                valid += int(bool(trace.citations) and set(trace.citations) <= set(retrieved))
                sentences = re.split(r"(?<=[.!?])\s+|\n+", trace.answer or "")
                uncited_sentences += sum(bool(s.strip()) and not re.search(r"\[C\d+\]", s) for s in sentences)
                decoys += sum(bool(retrieved[cid].is_decoy) for cid in trace.citations if cid in retrieved)
                unapproved += sum(not current().personal and not retrieved[cid].approved for cid in trace.citations if cid in retrieved)
        except Exception:
            errors += 1
    return {"oos_abstain_accuracy": oos_correct / oos if oos else None,
            "oos_total": oos, "oos_correct": oos_correct,
            "false_abstain_rate": false_abstains / answerable if answerable else None,
            "false_abstains": false_abstains, "total_answered": answered,
            "citation_validity_rate": valid / answered if answered else None,
            "decoy_citations": decoys, "unapproved_citations": unapproved, "errors": errors,
            "uncited_sentence_heuristic": uncited_sentences, "clarification_requests": clarifications}


async def evaluate_decoy_isolation(queries, mode, slow=0):
    """Retrieval-only comparison: unrestricted evaluation vs production filters."""
    rows = []
    for q in queries:
        if not eligible(q) or q.get("type") != "decoy_tempting":
            continue
        row = {"id": q["id"]}
        for production in (True, False):
            if slow:
                await asyncio.sleep(slow)
            try:
                result = await retrieve(q["query"], mode=mode, production=production)
                row["production" if production else "evaluation"] = {
                    "decoys_retrieved": sum(c.is_decoy for c in result.chunks),
                    "retrieved": len(result.chunks)}
            except Exception as exc:
                row["error"] = type(exc).__name__
        rows.append(row)
    return rows


def paired_raw_hyde(metrics):
    """Compare the same labelled questions; fallbacks are not HyDE evidence."""
    raw = {r['id']: r for r in metrics.get('raw', {}).get('observations', [])}
    hyde = {r['id']: r for r in metrics.get('hyde', {}).get('observations', [])}
    pairs, excluded = [], []
    for key in sorted(raw.keys() | hyde.keys()):
        a, b = raw.get(key), hyde.get(key)
        reason = ('missing_mode_result' if a is None or b is None else
                  'retrieval_error' if a.get('error') or b.get('error') else
                  'hyde_fell_back_to_raw' if b.get('hyde_failed') else None)
        if reason:
            excluded.append({'id': key, 'reason': reason})
            continue
        delta = b['reciprocal_rank'] - a['reciprocal_rank']
        pairs.append({'id': key, 'query': a.get('query', ''),
                      'raw_rr': a['reciprocal_rank'], 'hyde_rr': b['reciprocal_rank'],
                      'raw_recall_at_3': a['recall_at_3'], 'hyde_recall_at_3': b['recall_at_3'],
                      'outcome': 'win' if delta > 0 else 'loss' if delta < 0 else 'tie'})
    return {'n_pairs': len(pairs), 'wins': sum(p['outcome']=='win' for p in pairs),
            'ties': sum(p['outcome']=='tie' for p in pairs), 'losses': sum(p['outcome']=='loss' for p in pairs),
            'mean_rr_delta': mean([p['hyde_rr']-p['raw_rr'] for p in pairs]),
            'mean_recall_at_3_delta': mean([p['hyde_recall_at_3']-p['raw_recall_at_3'] for p in pairs]),
            'excluded': excluded, 'pairs': pairs,
            'interpretation': 'Retrieval only; positive delta favors HyDE. Excluded runs are availability failures, not evidence of retrieval quality. No semantic answer-accuracy claim.'}


def generate_markdown_report(results):
    metadata = results["metadata"]
    lines = ["# Benchmark report", "", f"Status: {metadata['status']}",
             f"Labels verified: {metadata['labels_verified']}",
             "Citation validity is syntactic; semantic faithfulness is not measured.",
             "Aggregate mode metrics include failures and Raw fallback outcomes. Use the complete paired comparison below to assess HyDE itself.", "",
             "| Mode | Recall@1 | Recall@3 | Recall@5 | MRR | Mean latency ms |", "|---|---|---|---|---|---|"]
    for mode, metrics in results["retrieval_metrics"].items():
        values = [metrics.get(k) for k in ("recall_at_1", "recall_at_3", "recall_at_5", "mrr", "mean_latency_ms")]
        lines.append("| " + mode + " | " + " | ".join("—" if v is None else f"{v:.3f}" for v in values) + " |")
    if not results["retrieval_metrics"]:
        lines.append("\nNo accuracy measurements: actual approved policies and verified labels are required.")
    paired = results.get('raw_hyde_comparison')
    if paired:
        lines.extend(['', '## Paired Raw versus HyDE', '',
                      f"Complete pairs: {paired['n_pairs']}; HyDE wins/ties/losses: {paired['wins']}/{paired['ties']}/{paired['losses']}; excluded: {len(paired['excluded'])}.",
                      paired['interpretation'], '', '| Question ID | Raw reciprocal rank | HyDE reciprocal rank | Outcome |', '|---|---:|---:|---|'])
        for p in paired['pairs']:
            key = str(p['id']).replace('|', r'\|').replace('\n', ' ')
            lines.append(f"| {key} | {p['raw_rr']:.3f} | {p['hyde_rr']:.3f} | {p['outcome']} |")
    for mode, metrics in results.get("safety_metrics", {}).items():
        lines.extend(["", f"## Safety: {mode}", "", "| Metric | Value |", "|---|---|"])
        lines.extend(f"| {key} | {value if value is not None else '—'} |" for key, value in metrics.items())
    return "\n".join(lines) + "\n"


def generate_svg(results):
    """Standalone chart; only measured values are drawn."""
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="720" height="340" viewBox="0 0 720 340">',
             '<rect width="720" height="340" fill="#101827"/>',
             '<g fill="#edf2fa" font-family="sans-serif"><text x="24" y="32">Measured retrieval recall@5 and MRR (0–1)</text>']
    if not results["retrieval_metrics"]:
        parts.append('<text x="24" y="90">Awaiting approved corpus and verified labels; no measurements.</text>')
    for i, (mode, metrics) in enumerate(results["retrieval_metrics"].items()):
        y = 80 + i * 75
        parts.append(f'<text x="24" y="{y}">{escape(mode)}</text>')
        for offset, metric, color in [(0, "recall_at_5", "#8c83ff"), (24, "mrr", "#51d2af")]:
            value = metrics.get(metric)
            if value is not None:
                parts.append(f'<rect x="120" y="{y - 14 + offset}" width="{max(0, min(1, value)) * 420:.2f}" height="18" fill="{color}"/>')
                parts.append(f'<text x="560" y="{y + offset}">{metric}: {value:.3f}</text>')
    parts.append('</g></svg>')
    return "".join(parts)


async def run_benchmark(modes=None, use_cache=True, slow=0):
    modes = list(MODES) if modes is None else modes
    if not modes or any(m not in MODES for m in modes):
        raise ValueError("Choose raw, hyde or fusion")
    queries = load_queries()
    labels_ready = bool(queries) and all(eligible(q) and not q.get("is_synthetic") for q in queries)
    corpus_ready = False
    if labels_ready:
        gold = list({cid for q in queries for cid in q.get("gold_chunk_ids", [])})
        corpus_ready = await asyncio.to_thread(has_chunks)
        if gold:
            corpus_ready = corpus_ready and await asyncio.to_thread(valid_cached_citations, gold)
    ready = labels_ready and corpus_ready
    started = time.perf_counter()
    results = {"retrieval_metrics": {}, "safety_metrics": {}, "decoy_isolation": {}, "metadata": {
        "workspace_id":current().workspace_id,"institution_id":current().institution_id,
        "timestamp": datetime.now(timezone.utc).isoformat(), "n_queries": len(queries),
        "labels_verified": labels_ready, "status": "completed" if ready else (
            "awaiting_approved_corpus" if labels_ready else "awaiting_verified_labels"),
        "confidence_threshold": CONFIDENCE_THRESHOLD, "evaluation_scope": "personal_unverified" if current().personal else "production",
        "hyde_cache_enabled": use_cache, "best_mode": None,
    }}
    token = cache_enabled.set(use_cache)
    try:
        if ready:
            for mode in modes:
                results["retrieval_metrics"][mode] = await evaluate_retrieval(queries, mode, use_cache, slow)
                results["safety_metrics"][mode] = await evaluate_safety(queries, mode, slow)
                results["decoy_isolation"][mode] = await evaluate_decoy_isolation(queries, mode, slow)
            results['raw_hyde_comparison'] = paired_raw_hyde(results['retrieval_metrics'])
            candidates = {m: r for m, r in results['retrieval_metrics'].items() if r['mrr'] is not None}
            complete = (len(candidates) == len(modes) and
                        not any(r['errors'] or r['hyde_failures'] for r in candidates.values()))
            if complete and len(candidates) > 1:
                best = max(r['mrr'] for r in candidates.values())
                winners = [m for m,r in candidates.items() if r['mrr'] == best]
                results['metadata']['best_mode'] = winners[0] if len(winners) == 1 else None
            results['metadata']['comparison_note'] = 'No unique winner is declared for tied scores, missing results or retrieval/HyDE failures; MRR is retrieval-only.'
            if any(m["errors"] or m["hyde_failures"] for m in results["retrieval_metrics"].values()) or any(m["errors"] for m in results["safety_metrics"].values()):
                results["metadata"]["status"] = "completed_with_errors"
    finally:
        cache_enabled.reset(token)
    results["metadata"]["elapsed_s"] = round(time.perf_counter() - started, 3)
    write_json(workspace_path("results") / "latest.json", results)
    (workspace_path("results") / "latest.md").write_text(generate_markdown_report(results))
    (workspace_path("results") / "latest.svg").write_text(generate_svg(results))
    print(f"Benchmark status: {results['metadata']['status']}")
    return results


async def main():
    parser = argparse.ArgumentParser()
    tenant=parser.add_mutually_exclusive_group(required=True)
    tenant.add_argument("--institution-id")
    tenant.add_argument("--workspace-id")
    parser.add_argument("--modes", nargs="+", choices=MODES)
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--slow", nargs="?", type=float, const=3.0, default=0)
    args = parser.parse_args()
    if args.slow < 0:
        parser.error("--slow must be nonnegative")
    ctx=__import__('src.personal',fromlist=['resolve']).resolve(args.workspace_id) if args.workspace_id else resolve(args.institution_id)
    with scope(ctx):
        await run_benchmark(args.modes, not args.no_cache, args.slow)


if __name__ == "__main__":
    asyncio.run(main())
