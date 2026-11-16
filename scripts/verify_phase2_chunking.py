#!/usr/bin/env python3
"""Verify Phase 2 chunk quality improvements in a disposable personal workspace."""
import json
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
import fitz
import httpx
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

CHILD_SERVER = r'''
import os
from pathlib import Path
from src import institutions, store, server
root = Path(os.environ['DISPOSABLE_DATA_ROOT'])
institutions.DATA_ROOT = root / 'data'
store.CHROMA_DIR = str(root / 'chroma')
server.RATE_LIMIT = 500
import uvicorn
uvicorn.run(server.app, host='127.0.0.1', port=int(os.environ['DISPOSABLE_PORT']), access_log=False, log_level='warning')
'''


def check_word_boundaries(raw_text: str) -> tuple[bool, str, str]:
    if not raw_text.strip():
        return True, "", ""
    text = raw_text.strip()
    first_char = text[0]
    starts_clean = True
    if first_char.isalpha() and first_char.islower():
        first_word = text.split()[0]
        if len(first_word) > 1 and first_word not in {"e.g.", "i.e.", "etc.", "v.", "vs."}:
            starts_clean = False
    last_char = text[-1]
    ends_clean = last_char in ".!?;:)]\"'0123456789" or text.split()[-1].isalnum()
    return starts_clean and ends_clean, text[:30], text[-30:]


def run_verification():
    pdf_paths = [
        PROJECT_ROOT / "audit_inputs" / "Examination_Rules.pdf",
        PROJECT_ROOT / "audit_inputs" / "NIT_Goa_Regulations.pdf",
    ]
    for p in pdf_paths:
        if not p.exists():
            raise FileNotFoundError(f"Missing PDF: {p}")

    with TemporaryDirectory(prefix="personal-chunk-audit-") as temp_dir:
        temp_root = Path(temp_dir)
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]

        env = dict(os.environ,
                   PYTHONPATH=str(PROJECT_ROOT),
                   DISPOSABLE_DATA_ROOT=str(temp_root),
                   DISPOSABLE_PORT=str(port))

        proc = subprocess.Popen(
            [sys.executable, "-c", CHILD_SERVER],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        base_url = f"http://127.0.0.1:{port}"
        client = httpx.Client(base_url=base_url, timeout=60.0)

        # Wait for server
        ready = False
        for _ in range(60):
            try:
                r = client.get("/health")
                if r.status_code == 200:
                    ready = True
                    break
            except Exception:
                pass
            time.sleep(0.2)

        if not ready:
            proc.terminate()
            raise RuntimeError("Disposable server failed to start.")

        print(f"[Phase 2] Disposable server started on port {port}.")

        try:
            # Create personal workspace
            ws_res = client.post("/personal/workspaces", json={"college": "Audit Disposable Workspace"})
            assert ws_res.status_code == 200, ws_res.text
            wid = ws_res.json()["workspace_id"]
            client.headers["X-Workspace-ID"] = wid
            print(f"[Phase 2] Created workspace: {wid}")

            # Upload & index documents
            doc_map = {}
            for pdf_path in pdf_paths:
                print(f"[Phase 2] Uploading {pdf_path.name}...")
                with open(pdf_path, "rb") as f:
                    up_res = client.post("/personal/documents", files={"files": (pdf_path.name, f, "application/pdf")})
                assert up_res.status_code == 200, up_res.text
                source = up_res.json()["documents"][0]["source"]
                doc_id = source["doc_id"]
                doc_map[pdf_path.name] = doc_id

                print(f"[Phase 2] Indexing {pdf_path.name} ({doc_id})...")
                idx_res = client.post(f"/personal/documents/{doc_id}/index", json={})
                assert idx_res.status_code == 200, idx_res.text
                print(f"  Indexed: {idx_res.json().get('chunks_added', 0)} chunks added.")

            # Retrieve chunks
            ev_res = client.get("/personal/evidence", params={"limit": 500})
            assert ev_res.status_code == 200, ev_res.text
            all_chunks = ev_res.json().get("chunks", [])
            print(f"[Phase 2] Total chunks indexed: {len(all_chunks)}")

            # Evaluate per-document metrics
            after_stats = {}
            for pdf_path in pdf_paths:
                doc = fitz.open(pdf_path)
                doc_chunks = [
                    c for c in all_chunks
                    if pdf_path.stem.replace("_", " ").lower() in c.get("doc_title", "").lower()
                    or pdf_path.name in c.get("source_path", "")
                ]
                word_counts = [len(c.get("raw_text", c["text"]).split()) for c in doc_chunks]
                mid_word_count = sum(not check_word_boundaries(c.get("raw_text", c["text"]))[0] for c in doc_chunks)
                near_empty_count = sum(len(c.get("raw_text", c["text"]).split()) < 10 for c in doc_chunks)
                generic_heading_count = sum(bool(re.match(r"^Page \d+$", c.get("section", ""))) for c in doc_chunks)

                after_stats[pdf_path.name] = {
                    "pages": len(doc),
                    "chunk_count": len(doc_chunks),
                    "words_min": int(min(word_counts)) if word_counts else 0,
                    "words_p25": int(np.percentile(word_counts, 25)) if word_counts else 0,
                    "words_median": int(np.median(word_counts)) if word_counts else 0,
                    "words_p75": int(np.percentile(word_counts, 75)) if word_counts else 0,
                    "words_max": int(max(word_counts)) if word_counts else 0,
                    "mid_word_boundary_chunks": mid_word_count,
                    "empty_or_near_empty_chunks": near_empty_count,
                    "generic_placeholder_headings": generic_heading_count,
                }

            # Run self-retrieval test on 20 sampled sentences
            print("\n[Phase 2] Running self-retrieval test on 20 sampled sentences...")
            sampled_sentences = []
            step = max(1, len(all_chunks) // 20)
            for i in range(0, len(all_chunks), step):
                if len(sampled_sentences) >= 20:
                    break
                c = all_chunks[i]
                sentences = [
                    s.strip() for s in re.split(r"[.!?]\s+", c.get("raw_text", c["text"]))
                    if len(s.strip().split()) >= 6 and len(s.strip()) > 30 and " > " not in s
                ]
                if sentences:
                    sampled_sentences.append((sentences[0], c["chunk_id"]))

            r1_hits = 0
            r3_hits = 0
            for q_sent, gold_cid in sampled_sentences:
                cmp_res = client.post("/personal/compare", json={"question": q_sent, "mode": "raw"})
                if cmp_res.status_code == 200:
                    ret_chunks = cmp_res.json().get("raw", {}).get("chunks", [])
                    ret_ids = [rc["chunk_id"] for rc in ret_chunks]
                    if ret_ids and ret_ids[0] == gold_cid:
                        r1_hits += 1
                    if gold_cid in ret_ids[:3]:
                        r3_hits += 1

            total_tested = len(sampled_sentences)
            self_r1_pct = (r1_hits / total_tested * 100) if total_tested else 0.0
            self_r3_pct = (r3_hits / total_tested * 100) if total_tested else 0.0
            print(f"[Phase 2] Self-retrieval: tested={total_tested}, R@1={self_r1_pct:.1f}%, Top-3={self_r3_pct:.1f}%")

            # Load before stats
            before_stats_path = PROJECT_ROOT / "audit" / "results" / "extraction_stats.json"
            before_stats = json.loads(before_stats_path.read_text()) if before_stats_path.exists() else {}

            before_embed_path = PROJECT_ROOT / "audit" / "results" / "embeddings_and_store.json"
            before_embed = json.loads(before_embed_path.read_text()) if before_embed_path.exists() else {}

            summary = {
                "before_stats": before_stats,
                "after_stats": after_stats,
                "self_retrieval_before": {
                    "r1_pct": before_embed.get("self_retrieval_r1_pct", 68.75),
                    "r3_pct": before_embed.get("self_retrieval_r3_pct", 90.625),
                },
                "self_retrieval_after": {
                    "tested": total_tested,
                    "r1_hits": r1_hits,
                    "r3_hits": r3_hits,
                    "r1_pct": self_r1_pct,
                    "r3_pct": self_r3_pct,
                },
            }

            out_path = PROJECT_ROOT / "audit" / "results" / "phase2_chunking_results.json"
            out_path.write_text(json.dumps(summary, indent=2))
            print(f"\n[Phase 2] Saved results to {out_path}")
            return summary

        finally:
            proc.terminate()
            proc.wait()


if __name__ == "__main__":
    run_verification()

