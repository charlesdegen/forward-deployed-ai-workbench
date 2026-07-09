"""Built-in red-team prompt suite categories and fixture loading."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CATEGORIES = (
    "prompt_injection",
    "jailbreak",
    "tool_boundary",
    "hallucination",
)

SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}


def load_suite(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Suite fixture must be a JSON array of cases")
    for case in data:
        _validate_case(case)
    return data


def _validate_case(case: dict[str, Any]) -> None:
    required = {"case_id", "category", "severity", "prompt", "expected_behavior", "pass_criteria"}
    missing = required.difference(case)
    if missing:
        raise ValueError(f"Case missing fields: {sorted(missing)}")
    if case["category"] not in CATEGORIES:
        raise ValueError(f"Unknown category: {case['category']}")
