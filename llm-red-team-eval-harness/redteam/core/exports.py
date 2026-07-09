"""Export red-team eval reports as JSON and markdown."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def build_report(
    results: list[dict[str, Any]],
    summary: dict[str, Any],
    *,
    data_source: str = "fixtures/redteam_suite.json",
    model_usage: str = "none (fixture responses / offline heuristics)",
) -> dict[str, Any]:
    return {
        "report_version": "1.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "governance": {
            "data_source": data_source,
            "model_usage": model_usage,
            "test_status": "pytest: redteam suite",
            "offline_default": True,
        },
        "assumptions": [
            "Default run uses fixture responses and heuristic pattern checks.",
            "Live model evaluation is optional and must be explicitly enabled by the operator.",
            "Failure patterns are illustrative, not an exhaustive red-team corpus.",
        ],
        "summary": summary,
        "results": results,
    }


def write_report(report: dict[str, Any], export_dir: str | Path) -> tuple[Path, Path]:
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = export_path / f"redteam_report_{stamp}.json"
    md_path = export_path / f"redteam_report_{stamp}.md"

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    s = report["summary"]
    lines = [
        "# LLM Red-Team Eval Report",
        "",
        f"Generated: {report['generated_at']}",
        f"Band: **{s['band']}** · Security score: **{s['security_score']}**",
        f"Passed: {s['passed']} / {s['total']} (rate {s['pass_rate']})",
        f"Model usage: {report['governance']['model_usage']}",
        "",
        "## By category",
        "",
    ]
    for cat, counts in s["by_category"].items():
        lines.append(f"- `{cat}`: pass {counts['pass']}, fail {counts['fail']}")
    lines.extend(["", "## Failed cases", ""])
    failures = [r for r in report["results"] if not r["passed"]]
    if not failures:
        lines.append("_None_")
    else:
        for r in failures:
            lines.append(
                f"- **{r['case_id']}** ({r['category']}/{r['severity']}): {r['expected_behavior']}"
            )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path
