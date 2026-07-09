#!/usr/bin/env python3
"""Capture README screenshots from portfolio surfaces (requires playwright)."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = REPO_ROOT / "artifacts" / "screenshots"


def _wait_for_server(url: str, attempts: int = 60) -> None:
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


def _screenshot_url(url: str, out_name: str, *, settle: float = 2.0) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url, wait_until="networkidle", timeout=60_000)
        time.sleep(settle)
        page.screenshot(path=str(SCREENSHOT_DIR / out_name), full_page=True)
        browser.close()


def _capture_nicegui_mission() -> None:
    process = subprocess.Popen(
        [sys.executable, str(REPO_ROOT / "src/apps/nicegui_app.py")],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_server("http://127.0.0.1:8080")
        time.sleep(2)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.goto("http://127.0.0.1:8080", wait_until="networkidle")
            time.sleep(2)
            page.screenshot(
                path=str(SCREENSHOT_DIR / "mission_console_overview.png"),
                full_page=True,
            )
            page.get_by_text("Operator Log", exact=True).click()
            time.sleep(1)
            page.screenshot(
                path=str(SCREENSHOT_DIR / "mission_console_operator_log.png"),
                full_page=True,
            )
            browser.close()
    finally:
        _terminate(process)


def _capture_streamlit_app(script: Path, port: int, out_name: str, *, cwd: Path | None = None) -> None:
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
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_server(f"http://127.0.0.1:{port}")
        time.sleep(3)
        _screenshot_url(f"http://127.0.0.1:{port}", out_name, settle=2.5)
    finally:
        _terminate(process)


def _capture_fusion() -> None:
    process = subprocess.Popen(
        [sys.executable, str(REPO_ROOT / "local-data-fusion-workbench/fusion/apps/nicegui_app.py")],
        cwd=REPO_ROOT / "local-data-fusion-workbench",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_server("http://127.0.0.1:8081")
        time.sleep(2)
        _screenshot_url("http://127.0.0.1:8081", "data_fusion_overview.png", settle=2.5)
    finally:
        _terminate(process)


def _capture_single_file_brief() -> None:
    path = (REPO_ROOT / "single-file-command-briefs" / "index.html").resolve().as_uri()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(path, wait_until="networkidle", timeout=60_000)
        time.sleep(1.5)
        page.screenshot(
            path=str(SCREENSHOT_DIR / "single_file_command_brief.png"),
            full_page=True,
        )
        browser.close()


def main() -> None:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    _capture_nicegui_mission()
    _capture_streamlit_app(
        REPO_ROOT / "src/apps/streamlit_app.py",
        8501,
        "streamlit_starter_overview.png",
    )
    _capture_fusion()
    _capture_streamlit_app(
        REPO_ROOT / "financial-crime-ops-console/fin_crime/apps/streamlit_app.py",
        8502,
        "fin_crime_overview.png",
        cwd=REPO_ROOT / "financial-crime-ops-console",
    )
    _capture_streamlit_app(
        REPO_ROOT / "llm-red-team-eval-harness/redteam/apps/streamlit_app.py",
        8503,
        "redteam_overview.png",
        cwd=REPO_ROOT / "llm-red-team-eval-harness",
    )
    _capture_single_file_brief()
    print(f"Screenshots saved to {SCREENSHOT_DIR}")
    for path in sorted(SCREENSHOT_DIR.glob("*.png")):
        print(f"  - {path.name}")


if __name__ == "__main__":
    main()
