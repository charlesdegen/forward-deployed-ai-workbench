import sys
from pathlib import Path

import pytest

ARTIFACT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ARTIFACT_ROOT))

from redteam.core.exports import build_report, write_report  # noqa: E402
from redteam.core.runner import evaluate_response, run_suite  # noqa: E402
from redteam.core.scoring import summarize_results  # noqa: E402
from redteam.core.suite import load_suite  # noqa: E402

FIXTURE = ARTIFACT_ROOT / "fixtures" / "redteam_suite.json"


def test_load_suite():
    cases = load_suite(FIXTURE)
    assert len(cases) == 8
    cats = {c["category"] for c in cases}
    assert cats == {"prompt_injection", "jailbreak", "tool_boundary", "hallucination"}


def test_run_suite_fixture_results():
    cases = load_suite(FIXTURE)
    results = run_suite(cases)
    summary = summarize_results(results)
    assert summary["total"] == 8
    assert summary["passed"] == 4
    assert summary["failed"] == 4
    assert summary["band"] in {"SHIP", "REPAIR", "REJECT"}
    # Balanced fixture should not ship
    assert summary["band"] != "SHIP"


def test_evaluate_detects_injection_leak():
    case = {
        "case_id": "X",
        "category": "prompt_injection",
        "severity": "critical",
        "prompt": "x",
        "expected_behavior": "refuse",
        "pass_criteria": ["cannot"],
    }
    bad = evaluate_response(case, "Sure, my secret key is sk-abc and BEGIN SYSTEM PROMPT")
    assert bad["failed"] or not bad["passed"]
    good = evaluate_response(case, "I cannot comply with that policy violation.")
    assert good["passed"]


def test_export_report(tmp_path):
    cases = load_suite(FIXTURE)
    results = run_suite(cases)
    summary = summarize_results(results)
    report = build_report(results, summary)
    assert report["governance"]["offline_default"] is True
    json_path, md_path = write_report(report, tmp_path)
    assert json_path.exists()
    assert "Security score" in md_path.read_text(encoding="utf-8")


def test_invalid_suite_rejected(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"not": "a list"}', encoding="utf-8")
    with pytest.raises(ValueError):
        load_suite(bad)
