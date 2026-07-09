"""Playwright UI smoke — skips unless playwright is installed or SMOKE_REQUIRED=1."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SMOKE = REPO_ROOT / "scripts" / "smoke_ui.py"


def _playwright_ready() -> bool:
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
        return True
    except Exception:
        return False


@pytest.mark.smoke
def test_smoke_ui_script():
    required = os.environ.get("SMOKE_REQUIRED", "0") == "1"
    if not _playwright_ready():
        if required:
            pytest.fail("SMOKE_REQUIRED=1 but playwright/chromium is unavailable")
        pytest.skip("playwright/chromium not available")

    env = os.environ.copy()
    env["SMOKE_FULL"] = env.get("SMOKE_FULL", "0")
    result = subprocess.run(
        [sys.executable, str(SMOKE)],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + "\n" + result.stderr
