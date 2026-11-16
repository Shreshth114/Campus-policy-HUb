#!/usr/bin/env python3
"""
Verify live Gemini failover end-to-end on a disposable instance with synthetic fixture.
Groq is forced to fail via test configuration (GROQ_BASE_URL pointed to unreachable local port),
so real Groq quota is never exhausted.
Zero keys or credentials are printed or logged.
"""
import asyncio
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from tempfile import TemporaryDirectory
import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

CHILD_SERVER = r'''
import os
from pathlib import Path
from src import institutions, store, server
root = Path(os.environ["PERSONAL_E2E_ROOT"])
institutions.DATA_ROOT = root / "data"
store.CHROMA_DIR = str(root / "chroma")
server.RATE_LIMIT = 300
import uvicorn
uvicorn.run(server.app, host="127.0.0.1", port=int(os.environ["PERSONAL_E2E_PORT"]), access_log=False, log_level="warning")
'''


def run_failover_e2e():
    print("================================================================")
    print(" LIVE GEMINI FAILOVER VERIFICATION (DISPOSABLE INSTANCE)")
    print(" Groq forced to fail via test config; live Gemini fallback")
    print("================================================================\n")

    with TemporaryDirectory(prefix="gemini-failover-e2e-") as tmpdir:
        root = Path(tmpdir)
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]

        # Force Groq to fail immediately via unreachable port without burning real Groq quota
        child_env = {
            **os.environ,
            "PERSONAL_E2E_ROOT": str(root),
            "PERSONAL_E2E_PORT": str(port),
            "GROQ_BASE_URL": "http://127.0.0.1:9999/v1",
            "LLM_TOTAL_WAIT_BUDGET": "8.0",
            "HF_HUB_OFFLINE": "1",
        }

        with (root / "server.log").open("w") as log_file:
            proc = subprocess.Popen(
                [sys.executable, "-u", "-c", CHILD_SERVER],
                cwd=str(PROJECT_ROOT),
                env=child_env,
                stdout=log_file,
                stderr=log_file,
            )

        client = httpx.Client(base_url=f"http://127.0.0.1:{port}", timeout=60.0)

        try:
            # 1. Wait for server readiness
            ready = False
            for _ in range(40):
                try:
                    r = client.get("/health")
                    if r.status_code == 200:
                        ready = True
                        break
                except Exception:
                    pass
                time.sleep(0.3)
            assert ready, "Disposable server failed to start within 12 seconds"
            print("✓ Disposable server running on ephemeral port", port)

            # 2. Create personal workspace and upload SYNTHETIC TEST FIXTURE A only (unambiguous)
            ws_resp = client.post("/personal/workspaces", json={"college": "SYNTHETIC TEST FIXTURE College A"})
            assert ws_resp.status_code == 200, f"Workspace creation failed: {ws_resp.text}"
            ws_data = ws_resp.json()
            ws_id = ws_data["workspace_id"]
            headers = {"X-Workspace-ID": ws_id}

            fixture_path = PROJECT_ROOT / "tests/fixtures/personal_demo/SYNTHETIC TEST FIXTURE A.pdf"
            up_resp = client.post(
                "/personal/documents",
                files={"files": ("SYNTHETIC TEST FIXTURE A.pdf", fixture_path.read_bytes(), "application/pdf")},
                headers=headers,
            )
            assert up_resp.status_code == 200, f"Upload failed: {up_resp.text}"
            doc_id = up_resp.json()["documents"][0]["source"]["doc_id"]

            idx_resp = client.post(f"/personal/documents/{doc_id}/index", headers=headers, json={})
            assert idx_resp.status_code == 200, f"Index failed: {idx_resp.text}"
            print(f"✓ Synthetic test fixture A loaded and indexed (workspace_id: {ws_id[:12]}...)")

            # 3. Ask policy question with raw mode (1 live Gemini call)
            q1 = "What attendance percentage is required in this fictional test document?"
            print(f"  Sending policy question: '{q1}' (Groq forced down)...")
            t0 = time.time()
            ask_resp = client.post("/personal/ask", json={"question": q1, "mode": "raw"}, headers=headers)
            lat = (time.time() - t0) * 1000
            assert ask_resp.status_code == 200, f"/personal/ask failed: {ask_resp.text}"
            trace = ask_resp.json()

            # Confirm Gemini answered and failover was recorded
            provider = trace.get("provider")
            decision = trace.get("decision")
            failovers = trace.get("failovers", 0)
            answer = trace.get("answer", "")
            citations = trace.get("citations", [])
            verified_quotes = trace.get("verified_quotes", [])

            print(f"✓ Provider: {provider} (expected: gemini)")
            print(f"✓ Decision: {decision} (expected: answered)")
            print(f"✓ Failovers recorded: {failovers} (expected: >= 1)")
            print(f"✓ Citations: {len(citations)} chunk(s) cited")
            print(f"✓ Quotes verified: {len(verified_quotes)} quote(s)")
            print(f"✓ Answer snippet: '{answer[:80]}...'")
            print(f"✓ Latency: {lat:.1f}ms")

            assert provider == "gemini", f"Expected provider 'gemini', got '{provider}'"
            assert decision == "answered", f"Expected decision 'answered', got '{decision}'"
            assert failovers >= 1, f"Expected failovers >= 1, got {failovers}"
            assert len(citations) > 0, "Expected at least one citation"
            assert len(verified_quotes) > 0, "Expected at least one verified quote"
            assert "75" in answer or "attendance" in answer.lower(), "Expected attendance answer content"

            # 4. Out-of-scope question: must safely abstain
            q2 = "What is the boiling point of liquid neon at standard pressure?"
            print(f"\n  Sending out-of-scope question: '{q2}'...")
            out_resp = client.post("/personal/ask", json={"question": q2, "mode": "raw"}, headers=headers)
            assert out_resp.status_code == 200
            out_trace = out_resp.json()

            out_decision = out_trace.get("decision")
            out_reason = out_trace.get("abstain_reason")
            print(f"✓ Out-of-scope decision: {out_decision} (expected: abstained)")
            print(f"✓ Out-of-scope reason: {out_reason}")
            assert out_decision == "abstained", f"Expected abstained, got {out_decision}"

            print("\n================================================================")
            print(" ALL REAL GEMINI FAILOVER CHECKS PASSED SUCCESSFULLY")
            print("================================================================")

        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    run_failover_e2e()
