#!/usr/bin/env python3
"""Capture README screenshots from local console surfaces (requires playwright)."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = REPO_ROOT / "artifacts" / "screenshots"


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


def _capture_nicegui() -> None:
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
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


def _capture_streamlit() -> None:
    process = subprocess.Popen(
        [
            "streamlit",
            "run",
            str(REPO_ROOT / "src/apps/streamlit_app.py"),
            "--server.headless",
            "true",
            "--server.port",
            "8501",
            "--browser.gatherUsageStats",
            "false",
        ],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_server("http://127.0.0.1:8501")
        time.sleep(3)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.goto("http://127.0.0.1:8501", wait_until="networkidle")
            time.sleep(2)
            page.screenshot(
                path=str(SCREENSHOT_DIR / "streamlit_starter_overview.png"),
                full_page=True,
            )
            browser.close()
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()


def main() -> None:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    _capture_nicegui()
    _capture_streamlit()
    print(f"Screenshots saved to {SCREENSHOT_DIR}")


if __name__ == "__main__":
    main()