"""Evidence packet and SAR narrative draft exports (synthetic / training only)."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

DEFAULT_ASSUMPTIONS = [
    "All counterparties and accounts are synthetic fixtures — not real persons.",
    "Risk scores are rule-based thresholds, not ML model outputs.",
    "SAR narrative drafts are training templates and not filed reports.",
    "No live bank systems or customer data were accessed.",
]


def build_evidence_packet(
    case_row: pd.Series | dict[str, Any],
    audit_log: pd.DataFrame | None = None,
    *,
    data_source: str = "fixtures/sample_transactions.csv",
) -> dict[str, Any]:
    if isinstance(case_row, pd.Series):
        case = case_row.to_dict()
    else:
        case = dict(case_row)

    # Normalize timestamps for JSON
    for key, value in list(case.items()):
        if hasattr(value, "isoformat"):
            case[key] = value.isoformat()

    actions: list[dict[str, Any]] = []
    if audit_log is not None and not audit_log.empty:
        tid = str(case.get("transaction_id", ""))
        subset = audit_log[audit_log["transaction_id"].astype(str) == tid]
        actions = subset.to_dict(orient="records")
        for action in actions:
            for k, v in list(action.items()):
                if hasattr(v, "isoformat"):
                    action[k] = v.isoformat()

    flags = str(case.get("risk_flags", "none")).split("|")
    narrative = (
        f"Synthetic alert review for transaction {case.get('transaction_id')}: "
        f"account {case.get('account_id')} initiated a {case.get('channel')} transfer of "
        f"USD {case.get('amount_usd')} from {case.get('country_origin')} to {case.get('country_dest')}. "
        f"Rule-based risk score {case.get('risk_score')} ({case.get('risk_band')}) triggered on flags: "
        f"{', '.join(flags)}. This draft is for operator training only and is not a regulatory filing."
    )

    return {
        "packet_version": "1.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "packet_type": "financial_crime_evidence",
        "governance": {
            "data_source": data_source,
            "model_usage": "none (rule-based scoring)",
            "test_status": "pytest: fin_crime suite",
            "synthetic_data": True,
        },
        "assumptions": DEFAULT_ASSUMPTIONS,
        "case": case,
        "audit_trail": actions,
        "sar_narrative_draft": narrative,
        "recommended_next_steps": [
            "Confirm customer identity documentation is complete (synthetic checklist).",
            "Request source-of-funds narrative from relationship manager (training).",
            "Escalate if risk_band is CRITICAL and prior_sar_count > 0.",
            "Export evidence packet and attach to case management system.",
        ],
    }


def write_evidence_exports(packet: dict[str, Any], export_dir: str | Path) -> tuple[Path, Path]:
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    tid = packet.get("case", {}).get("transaction_id", "unknown")
    json_path = export_path / f"evidence_{tid}_{stamp}.json"
    md_path = export_path / f"evidence_{tid}_{stamp}.md"

    json_path.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    md_lines = [
        f"# Evidence Packet — {tid}",
        "",
        f"Generated: {packet['generated_at']}",
        f"Data source: {packet['governance']['data_source']}",
        f"Synthetic: {packet['governance']['synthetic_data']}",
        "",
        "## SAR narrative draft (training only)",
        "",
        packet["sar_narrative_draft"],
        "",
        "## Case fields",
        "",
        "```json",
        json.dumps(packet["case"], indent=2),
        "```",
        "",
        "## Recommended next steps",
        "",
    ]
    for step in packet["recommended_next_steps"]:
        md_lines.append(f"- {step}")
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return json_path, md_path
