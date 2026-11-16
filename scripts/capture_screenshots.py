#!/usr/bin/env python3
"""Capture desktop (1440px) and mobile (390px) screenshots of all 13 tabs.

Ensures real or synthetic content is visible in each tab.
"""
import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = Path(__file__).resolve().parents[1] / "docs" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

VIEWS = [
    "home",
    "documents",
    "rulebook",
    "analysis",
    "conflicts",
    "changes",
    "compare",
    "bench",
    "evidence",
    "labels",
    "metrics",
    "how",
    "sources",
]


def capture_all():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # We will capture desktop first, then mobile
        configs = [
            ("1440", {"width": 1440, "height": 900}),
            ("390", {"width": 390, "height": 844}),
        ]

        for prefix, vp in configs:
            print(f"\n--- Capturing {prefix}px viewport ---")
            page = browser.new_page(viewport=vp)
            page.goto("http://127.0.0.1:8000")
            page.wait_for_load_state("networkidle")

            # 1. Load synthetic demo workspace so all personal tabs have content
            try:
                page.click("#personal-demo", timeout=3000)
                page.wait_for_timeout(1500)
            except Exception as e:
                print("Note on personal-demo click:", e)

            # 2. Extract rules if on rulebook
            try:
                page.evaluate("""() => {
                    if (window.personalWorkspaceId && typeof loadRules === 'function') {
                        loadRules();
                    }
                }""")
            except Exception:
                pass

            for v in VIEWS:
                # Switch view
                page.evaluate(f"""() => {{
                    const btn = document.querySelector(`[data-view="{v}"]`);
                    if (btn) {{
                        btn.click();
                    }} else {{
                        document.querySelectorAll('.view').forEach(el => el.hidden = true);
                        const target = document.getElementById('view-' + '{v}');
                        if (target) target.hidden = false;
                    }}
                }}""")
                page.wait_for_timeout(800)

                # Special view preparations to ensure rich content
                if v == "compare":
                    page.evaluate("""() => {
                        const input = document.getElementById('compare-q');
                        if (input && !input.value) {
                            input.value = "What are the attendance requirements?";
                            document.getElementById('compare-btn').click();
                        }
                    }""")
                    try:
                        page.wait_for_selector("#compare-btn:not([disabled])", timeout=7000)
                    except Exception:
                        pass
                    page.wait_for_timeout(500)

                elif v == "labels":
                    page.evaluate("""() => {
                        if (typeof loadLabels === 'function') loadLabels();
                    }""")
                    page.wait_for_timeout(800)

                elif v == "evidence":
                    page.evaluate("""() => {
                        if (typeof loadEvidence === 'function') loadEvidence();
                    }""")
                    page.wait_for_timeout(600)

                elif v == "metrics":
                    page.evaluate("""() => {
                        if (typeof renderMetrics === 'function') renderMetrics();
                    }""")
                    page.wait_for_timeout(400)

                elif v == "sources":
                    # Unlock admin view to show rich admin UI if possible
                    page.evaluate("""() => {
                        const input = document.getElementById('admin-token');
                        if (input) {
                            // Emulate unlocked state for demonstration capture
                            const authPanel = document.getElementById('admin-auth-panel');
                            const controls = document.getElementById('admin-controls');
                            if (authPanel) authPanel.hidden = true;
                            if (controls) controls.hidden = false;
                        }
                    }""")
                    page.wait_for_timeout(400)

                # Check horizontal overflow
                sw = page.evaluate("() => document.documentElement.scrollWidth")
                bw = page.evaluate("() => document.body.scrollWidth")
                max_w = max(sw, bw)
                target_w = vp["width"]

                img_path = SCREENSHOTS_DIR / f"{prefix}-{v}.png"
                page.screenshot(path=str(img_path), full_page=True)

                status = "OK" if max_w <= target_w else f"OVERFLOW ({max_w}px > {target_w}px)"
                print(f"  [{status}] {img_path.name} (scrollWidth: {max_w}px)")

            page.close()
        browser.close()
        print("\nAll screenshots captured successfully.")


if __name__ == "__main__":
    capture_all()
