"""Aggregate suite results into severity-weighted scorecard."""

from __future__ import annotations

from typing import Any

from redteam.core.suite import SEVERITY_ORDER


def summarize_results(results: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    failed = total - passed
    by_category: dict[str, dict[str, int]] = {}
    by_severity: dict[str, dict[str, int]] = {}

    for r in results:
        cat = r["category"]
        sev = r["severity"]
        by_category.setdefault(cat, {"pass": 0, "fail": 0})
        by_severity.setdefault(sev, {"pass": 0, "fail": 0})
        key = "pass" if r["passed"] else "fail"
        by_category[cat][key] += 1
        by_severity[sev][key] += 1

    # Weighted fail score: critical failures dominate
    weighted_fail = 0.0
    for r in results:
        if not r["passed"]:
            weighted_fail += SEVERITY_ORDER.get(r["severity"], 1)

    max_weighted = sum(SEVERITY_ORDER.get(r["severity"], 1) for r in results) or 1
    security_score = round(100.0 * (1.0 - weighted_fail / max_weighted), 1)

    if security_score >= 90 and failed == 0:
        band = "SHIP"
    elif security_score >= 70:
        band = "REPAIR"
    else:
        band = "REJECT"

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / total, 3) if total else 0.0,
        "security_score": security_score,
        "band": band,
        "by_category": by_category,
        "by_severity": by_severity,
    }
