import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.core.ingestion import alert_mask, summarize_alert_state

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"
DEFAULT_ASSUMPTIONS = [
    "Sensor frequency assumed 1 Hz when not specified in source metadata.",
    "Risk scoring uses thresholds defined in specs/data_contract.md.",
    "Operator actions reflect human-approved field steps only.",
    "No live LLM inference was used to produce this packet unless model_usage states otherwise.",
]


def _iso_timestamp(value) -> str:
    if pd.isna(value):
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return pd.Timestamp(value).strftime("%Y-%m-%dT%H:%M:%SZ")


def _row_to_alert_record(row: pd.Series) -> dict[str, Any]:
    return {
        "timestamp": _iso_timestamp(row["timestamp"]),
        "cpu_utilization": float(row["cpu_utilization"]),
        "temperature": float(row["temperature"]),
        "battery_level": float(row["battery_level"]),
        "sensor_drift": float(row["sensor_drift"]),
        "comms_link": float(row["comms_link"]),
        "risk_score": int(row["risk_score"]),
        "flags": {
            "cpu_anomaly": bool(row["cpu_anomaly"]),
            "temp_warning": bool(row["temp_warning"]),
            "temp_critical": bool(row["temp_critical"]),
            "sensor_anomaly": bool(row["sensor_anomaly"]),
            "comms_anomaly": bool(row["comms_anomaly"]),
        },
    }


def _recommendations_for_alert(alert: dict[str, Any]) -> list[str]:
    recs: list[str] = []
    flags = alert.get("flags", {})
    if flags.get("temp_critical") or flags.get("temp_warning"):
        recs.append("Verify cooling path and consider degraded-mode throttle or shutdown per triage-skill.")
    if flags.get("cpu_anomaly"):
        recs.append("Inspect compute processes for orphan high-CPU threads; capture process list for engineering.")
    if flags.get("sensor_anomaly"):
        recs.append("Schedule sensor recalibration; compare drift trend against baseline logs.")
    if flags.get("comms_anomaly"):
        recs.append("Check line-of-sight, antenna alignment, and comms link quality at alert timestamp.")
    if not recs:
        recs.append("Review raw telemetry with engineering; no threshold flags set on primary finding.")
    recs.append("Attach operator action log and git diff if repository changes were made during triage.")
    return recs


def build_rca_packet(
    scored_df: pd.DataFrame,
    data_source: str,
    operator_log: pd.DataFrame | None = None,
    assumptions: list[str] | None = None,
    *,
    test_status: str = "pytest: ingestion + golden suite",
    model_usage: str = "none (local scoring)",
    export_version: str = "1.0",
    packet_version: str = "1.0",
) -> dict[str, Any]:
    """Build an engineering RCA packet from scored telemetry and optional operator log."""
    alert_rows = scored_df[alert_mask(scored_df)].sort_values("risk_score", ascending=False)
    alerts = [_row_to_alert_record(row) for _, row in alert_rows.iterrows()]
    primary_finding = alerts[0] if alerts else None

    operator_actions: list[dict[str, Any]] = []
    if operator_log is not None and not operator_log.empty:
        operator_actions = operator_log.to_dict(orient="records")

    state = summarize_alert_state(scored_df)
    alert_count = state["alert_count"]
    system_state = state["system_state"]

    packet = {
        "packet_version": packet_version,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "governance": {
            "data_source": data_source,
            "record_count": int(len(scored_df)),
            "time_range": {
                "start": _iso_timestamp(scored_df["timestamp"].min()),
                "end": _iso_timestamp(scored_df["timestamp"].max()),
            },
            "system_state": system_state,
            "alert_count": alert_count,
            "test_status": test_status,
            "model_usage": model_usage,
            "export_version": export_version,
        },
        "assumptions": assumptions or DEFAULT_ASSUMPTIONS,
        "alerts": alerts,
        "operator_actions": operator_actions,
        "primary_finding": primary_finding,
        "recommendations": _recommendations_for_alert(primary_finding) if primary_finding else [
            "No scored alerts in telemetry window; confirm ingest source and threshold configuration."
        ],
    }
    return packet


def format_rca_markdown(packet: dict[str, Any]) -> str:
    """Render an RCA packet as markdown for engineering handoff."""
    gov = packet["governance"]
    lines = [
        "# RCA Packet — Mission Autonomy Field Support",
        "",
        f"**Generated:** {packet['generated_at']}",
        f"**Packet version:** {packet['packet_version']}",
        "",
        "## Governance",
        f"- Data source: `{gov['data_source']}`",
        f"- Records: {gov['record_count']}",
        f"- Time range: {gov['time_range']['start']} → {gov['time_range']['end']}",
        f"- System state: **{gov['system_state']}** ({gov['alert_count']} alerts)",
        f"- Test status: {gov['test_status']}",
        f"- Model usage: {gov['model_usage']}",
        "",
        "## Assumptions",
    ]
    lines.extend(f"- {item}" for item in packet["assumptions"])
    lines.append("")
    lines.append("## Primary finding")
    if packet["primary_finding"]:
        pf = packet["primary_finding"]
        lines.append(f"- Timestamp: {pf['timestamp']}")
        lines.append(f"- Risk score: {pf['risk_score']}")
        lines.append(f"- CPU: {pf['cpu_utilization']:.1f}% | Temp: {pf['temperature']:.1f}°C")
        lines.append(f"- Flags: `{pf['flags']}`")
    else:
        lines.append("- No alerts scored in window.")
    lines.append("")
    lines.append("## Recommendations")
    lines.extend(f"- {rec}" for rec in packet["recommendations"])
    lines.append("")
    lines.append("## Alert summary")
    if packet["alerts"]:
        for alert in packet["alerts"]:
            lines.append(
                f"- {alert['timestamp']}: risk={alert['risk_score']} "
                f"cpu={alert['cpu_utilization']:.1f}% temp={alert['temperature']:.1f}°C"
            )
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Operator actions")
    if packet["operator_actions"]:
        for action in packet["operator_actions"]:
            lines.append(
                f"- {action.get('timestamp', 'unknown')}: "
                f"[{action.get('disposition', 'n/a')}] {action.get('action', '')}"
            )
    else:
        lines.append("- No operator actions recorded.")
    lines.append("")
    return "\n".join(lines)


def load_schema(name: str) -> dict[str, Any]:
    path = SCHEMA_DIR / name
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_rca_exports(
    packet: dict[str, Any],
    export_dir: str | os.PathLike[str],
    *,
    basename: str | None = None,
) -> dict[str, str]:
    """Write JSON and markdown RCA exports; returns output paths."""
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = basename or f"rca_packet_{stamp}"

    json_path = export_path / f"{stem}.json"
    md_path = export_path / f"{stem}.md"

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)
        handle.write("\n")

    md_path.write_text(format_rca_markdown(packet), encoding="utf-8")

    return {"json": str(json_path), "markdown": str(md_path)}