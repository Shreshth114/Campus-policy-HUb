#!/usr/bin/env python3
"""Run and evaluate rule extraction on the audit corpus in a disposable workspace using in-process TestClient."""
import json
import os
import random
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src import institutions, store, server


def run_rule_verification():
    pdf_paths = [
        PROJECT_ROOT / "audit_inputs" / "Examination_Rules.pdf",
        PROJECT_ROOT / "audit_inputs" / "NIT_Goa_Regulations.pdf",
    ]
    for p in pdf_paths:
        if not p.exists():
            raise FileNotFoundError(f"Missing PDF: {p}")

    with TemporaryDirectory(prefix="personal-rule-audit-") as temp_dir:
        temp_root = Path(temp_dir)
        orig_data = institutions.DATA_ROOT
        orig_chroma = store.CHROMA_DIR

        institutions.DATA_ROOT = temp_root / "data"
        store.CHROMA_DIR = str(temp_root / "chroma")
        server.RATE_LIMIT = 500

        try:
            with TestClient(server.app) as client:
                print("[Phase 3] In-process client initialized with disposable storage.")

                # Create personal workspace
                ws_res = client.post("/personal/workspaces", json={"college": "Rule Audit Workspace"})
                assert ws_res.status_code == 200, ws_res.text
                wid = ws_res.json()["workspace_id"]
                headers = {"X-Workspace-ID": wid}
                print(f"[Phase 3] Created disposable workspace: {wid}")

                # Upload & index documents
                doc_map = {}
                for pdf_path in pdf_paths:
                    print(f"[Phase 3] Uploading {pdf_path.name}...")
                    with open(pdf_path, "rb") as f:
                        up_res = client.post(
                            "/personal/documents",
                            headers=headers,
                            files={"files": (pdf_path.name, f, "application/pdf")},
                        )
                    assert up_res.status_code == 200, up_res.text
                    source = up_res.json()["documents"][0]["source"]
                    doc_id = source["doc_id"]
                    doc_map[pdf_path.name] = doc_id

                    print(f"[Phase 3] Indexing {pdf_path.name}...")
                    idx_res = client.post(f"/personal/documents/{doc_id}/index", headers=headers, json={})
                    assert idx_res.status_code == 200, idx_res.text
                    print(f"  Indexed: {idx_res.json().get('chunks_added', 0)} chunks added.")

                # Run rule extraction per document
                print("\n[Phase 3] Running rule extraction on audit corpus...")
                t0 = time.time()
                extract_summaries = []
                for pdf_path in pdf_paths:
                    doc_id = doc_map[pdf_path.name]
                    print(f"[Phase 3] Extracting rules for {pdf_path.name}...")
                    t_doc = time.time()
                    ext_res = client.post("/personal/rules/extract", headers=headers, json={"document_id": doc_id})
                    assert ext_res.status_code == 200, ext_res.text
                    summary_item = ext_res.json()
                    print(f"  {pdf_path.name} finished in {time.time()-t_doc:.1f}s: {summary_item}")
                    extract_summaries.append(summary_item)

                elapsed_s = time.time() - t0
                print(f"\n[Phase 3] Total extraction time: {elapsed_s:.1f}s.")

                extract_summary = {
                    "documents": sum(s.get("documents", 0) for s in extract_summaries),
                    "rules": sum(s.get("rules", 0) for s in extract_summaries),
                    "discarded": sum(s.get("discarded", 0) for s in extract_summaries),
                    "cached_documents": sum(s.get("cached_documents", 0) for s in extract_summaries),
                    "errors": [e for s in extract_summaries for e in s.get("errors", [])],
                    "total_chunks_evaluated": sum(s.get("total_chunks_evaluated", 0) for s in extract_summaries),
                    "chunks_sent": sum(s.get("chunks_sent", 0) for s in extract_summaries),
                }

                # Fetch all rules
                rules_res = client.get("/personal/rules", headers=headers)
                assert rules_res.status_code == 200, rules_res.text
                rules = rules_res.json().get("rules", [])
                print(f"[Phase 3] Total validated rules in workspace: {len(rules)}")

                per_doc = {}
                for pdf_path in pdf_paths:
                    doc_name = pdf_path.stem.replace("_", " ").title()
                    doc_rules = [
                        r for r in rules
                        if r.get("document", "").lower() == doc_name.lower()
                        or pdf_path.stem.lower() in r.get("document", "").lower()
                    ]
                    per_doc[pdf_path.name] = {
                        "rule_count": len(doc_rules),
                        "rules": doc_rules,
                    }
                    print(f"  {pdf_path.name}: {len(doc_rules)} rules extracted")

                total_eval = extract_summary.get("total_chunks_evaluated", 0)
                chunks_sent = extract_summary.get("chunks_sent", 0)
                filter_rate = ((total_eval - chunks_sent) / total_eval * 100) if total_eval else 0.0

                total_accepted = extract_summary.get("rules", len(rules))
                total_discarded = extract_summary.get("discarded", 0)
                total_proposals = total_accepted + total_discarded
                validation_pass_rate = (total_accepted / total_proposals * 100) if total_proposals else 0.0

                # Sample 15 rules for manual evaluation
                random.seed(42)
                sampled_rules = random.sample(rules, min(15, len(rules))) if rules else []

                report_data = {
                    "elapsed_seconds": round(elapsed_s, 2),
                    "extraction_summary": extract_summary,
                    "total_chunks_evaluated": total_eval,
                    "chunks_sent_to_llm": chunks_sent,
                    "chunks_skipped": total_eval - chunks_sent,
                    "filter_rate_pct": round(filter_rate, 2),
                    "total_rules_extracted": len(rules),
                    "total_discarded": total_discarded,
                    "validation_pass_rate_pct": round(validation_pass_rate, 2),
                    "rules_per_document": {k: v["rule_count"] for k, v in per_doc.items()},
                    "sampled_15_rules": [
                        {
                            "rule_id": r.get("rule_id"),
                            "document": r.get("document"),
                            "page": r.get("page"),
                            "subject": r.get("subject"),
                            "operator": r.get("operator"),
                            "value": r.get("value"),
                            "unit": r.get("unit"),
                            "verbatim_quote": r.get("verbatim_quote"),
                            "applies_to": r.get("applies_to"),
                            "exceptions": r.get("exceptions"),
                            "deadline": r.get("deadline"),
                            "penalty": r.get("penalty"),
                        }
                        for r in sampled_rules
                    ],
                    "all_rules": rules,
                }

                out_file = PROJECT_ROOT / "audit" / "results" / "phase3_rule_extraction.json"
                out_file.write_text(json.dumps(report_data, indent=2))
                print(f"\n[Phase 3] Saved rule extraction results to {out_file}")
                return report_data
        finally:
            institutions.DATA_ROOT = orig_data
            store.CHROMA_DIR = orig_chroma


if __name__ == "__main__":
    run_rule_verification()
