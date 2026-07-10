#!/usr/bin/env python3
"""Playwright smoke checks for portfolio UIs.

Exit 0 on success. Skips cleanly when playwright/chromium is unavailable unless
SMOKE_REQUIRED=1 (then fail). Used by tests/test_smoke_ui.py and verify.sh.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _playwright_available() -> bool:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401

        return True
    except Exception:
        return False


def _wait_for_server(url: str, attempts: int = 45) -> None:
    import urllib.error
    import urllib.request

    for _ in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status < 500:
                    return
        except (urllib.error.URLError, TimeoutError):
            time.sleep(1)
    raise RuntimeError(f"Server did not become ready: {url}")


def _terminate(process: subprocess.Popen) -> None:
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()


def smoke_single_file_brief() -> None:
    from playwright.sync_api import sync_playwright

    path = (REPO_ROOT / "single-file-command-briefs" / "index.html").resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(path, wait_until="domcontentloaded", timeout=30_000)
        title = page.title()
        assert "Command Brief" in title or "Executive" in title, title
        state = page.locator("#metric-state").inner_text(timeout=10_000)
        assert state.strip(), "system state metric empty"
        # Offline: no network for chart if echarts local
        assert page.locator("#chart").count() == 1
        browser.close()


def smoke_mission_console() -> None:
    from playwright.sync_api import sync_playwright

    process = subprocess.Popen(
        [sys.executable, str(REPO_ROOT / "src/apps/nicegui_app.py")],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_server("http://127.0.0.1:8080")
        time.sleep(1)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("http://127.0.0.1:8080", wait_until="networkidle", timeout=60_000)
            body = page.content()
            assert "Mission" in body or "Governance" in body or "Alert" in body or "telemetry" in body.lower()
            browser.close()
    finally:
        _terminate(process)


def _smoke_streamlit(
    script: Path,
    port: int,
    needles: tuple[str, ...],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> None:
    from playwright.sync_api import sync_playwright

    process = subprocess.Popen(
        [
            "streamlit",
            "run",
            str(script),
            "--server.headless",
            "true",
            "--server.port",
            str(port),
            "--browser.gatherUsageStats",
            "false",
        ],
        cwd=str(cwd or REPO_ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_server(f"http://127.0.0.1:{port}")
        time.sleep(2)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(f"http://127.0.0.1:{port}", wait_until="networkidle", timeout=60_000)
            text = page.content()
            assert any(needle in text for needle in needles), f"none of {needles} rendered"
            browser.close()
    finally:
        _terminate(process)


def smoke_streamlit_starter() -> None:
    # Offline fallback constraint: the starter must serve without API credentials.
    env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
    _smoke_streamlit(
        REPO_ROOT / "src/apps/streamlit_app.py",
        8511,
        ("Mission Autonomy", "Telemetry"),
        env=env,
    )


def smoke_fin_crime() -> None:
    _smoke_streamlit(
        REPO_ROOT / "financial-crime-ops-console/fin_crime/apps/streamlit_app.py",
        8512,
        ("Financial Crime", "Case"),
        cwd=REPO_ROOT / "financial-crime-ops-console",
    )


def smoke_redteam() -> None:
    _smoke_streamlit(
        REPO_ROOT / "llm-red-team-eval-harness/redteam/apps/streamlit_app.py",
        8513,
        ("Red-Team", "Eval Harness"),
        cwd=REPO_ROOT / "llm-red-team-eval-harness",
    )


def smoke_fusion() -> None:
    from playwright.sync_api import sync_playwright

    process = subprocess.Popen(
        [sys.executable, str(REPO_ROOT / "local-data-fusion-workbench/fusion/apps/nicegui_app.py")],
        cwd=REPO_ROOT / "local-data-fusion-workbench",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_server("http://127.0.0.1:8081")
        time.sleep(1)
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("http://127.0.0.1:8081", wait_until="networkidle", timeout=60_000)
            body = page.content()
            assert "Fusion" in body or "Lineage" in body or "Profile" in body
            browser.close()
    finally:
        _terminate(process)


def main() -> int:
    required = os.environ.get("SMOKE_REQUIRED", "0") == "1"
    if not _playwright_available():
        msg = "playwright not installed"
        if required:
            print(f"FAIL: {msg}", file=sys.stderr)
            return 1
        print(f"SKIP: {msg}")
        return 0

    checks = [
        ("single-file-command-brief", smoke_single_file_brief),
        ("mission-console", smoke_mission_console),
        ("streamlit-starter", smoke_streamlit_starter),
        ("fusion", smoke_fusion),
        ("fin-crime", smoke_fin_crime),
        ("redteam", smoke_redteam),
    ]
    # Fast path for CI lite: only static brief unless SMOKE_FULL=1
    if os.environ.get("SMOKE_FULL", "0") != "1":
        checks = [checks[0]]

    failed = []
    for name, fn in checks:
        try:
            print(f"==> smoke {name}")
            fn()
            print(f"OK  {name}")
        except Exception as exc:  # noqa: BLE001 — surface any smoke failure
            print(f"FAIL {name}: {exc}", file=sys.stderr)
            failed.append(name)

    if failed:
        print(f"Smoke failures: {', '.join(failed)}", file=sys.stderr)
        return 1
    # Stamp for pre-commit / agent hooks
    stamp = REPO_ROOT / "artifacts" / ".verify_smoke_ok"
    stamp.parent.mkdir(parents=True, exist_ok=True)
    stamp.write_text(str(time.time()), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
