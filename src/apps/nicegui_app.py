"""Mission Autonomy Field Support Console — NiceGUI + DuckDB operator surface."""

from __future__ import annotations

import json
import sys
from datetime import timezone
from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from nicegui import ui

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.core.duckdb_store import (  # noqa: E402
    DEFAULT_DB_PATH,
    connect,
    fetch_alerts,
    fetch_scored_telemetry,
    fetch_summary,
    store_scored_telemetry,
)
from src.core.exports import build_rca_packet, format_rca_markdown, write_rca_exports  # noqa: E402
from src.core.ingestion import (  # noqa: E402
    TEMP_CRITICAL_THRESHOLD,
    TEMP_WARNING_THRESHOLD,
    generate_mock_telemetry,
    load_telemetry_csv,
    parse_telemetry_csv,
    score_anomalies,
)

DEFAULT_FIXTURE = REPO_ROOT / "fixtures" / "sample_telemetry.csv"
ACTION_LOG_PATH = REPO_ROOT / "artifacts" / "operator_action_log.csv"
EXPORT_DIR = REPO_ROOT / "artifacts" / "exports"

STATE: dict = {
    "data_source": "fixtures/sample_telemetry.csv",
    "summary": {},
    "scored_df": pd.DataFrame(),
    "degraded_mode": False,
}


def _load_operator_log() -> pd.DataFrame | None:
    if ACTION_LOG_PATH.exists():
        return pd.read_csv(ACTION_LOG_PATH)
    return None


def _ingest_source(source_mode: str, upload_bytes: bytes | None = None, upload_name: str = "") -> None:
    if source_mode == "Mock (synthetic)":
        raw = generate_mock_telemetry(50)
        label = "simulated_telemetry_v1"
    elif source_mode == "Fixture (sample_telemetry.csv)":
        raw = load_telemetry_csv(DEFAULT_FIXTURE)
        label = "fixtures/sample_telemetry.csv"
    else:
        if not upload_bytes:
            ui.notify("Upload a CSV before ingesting.", type="warning")
            return
        raw = parse_telemetry_csv(BytesIO(upload_bytes))
        label = upload_name or "uploaded_telemetry.csv"

    scored = score_anomalies(raw)
    conn = connect(DEFAULT_DB_PATH)
    try:
        store_scored_telemetry(conn, scored, label)
        STATE["data_source"] = label
        STATE["scored_df"] = fetch_scored_telemetry(conn)
        STATE["summary"] = fetch_summary(conn)
    finally:
        conn.close()


def _metric_card(title: str, value: str, subtitle: str, accent: str = "#e6edf3") -> None:
    with ui.card().classes("w-full bg-[#171a21] border border-[#232733] p-4"):
        ui.label(title).classes("text-xs uppercase tracking-wide text-[#8b949e]")
        ui.label(value).classes("text-2xl font-bold").style(f"color: {accent}")
        ui.label(subtitle).classes("text-[10px] text-[#484f58] mt-1")


def _build_timeline_figure(df: pd.DataFrame) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["cpu_utilization"],
            name="CPU %",
            line={"color": "#58a6ff"},
        )
    )
    figure.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["temperature"],
            name="Temp °C",
            yaxis="y2",
            line={"color": "#f0883e"},
        )
    )
    figure.add_trace(
        go.Scatter(
            x=df["timestamp"],
            y=df["battery_level"],
            name="Battery %",
            line={"color": "#3fb950"},
        )
    )
    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f1115",
        plot_bgcolor="#0f1115",
        margin={"l": 40, "r": 40, "t": 30, "b": 40},
        height=360,
        legend={"orientation": "h"},
        yaxis={"title": "CPU / Battery"},
        yaxis2={
            "title": "Temp °C",
            "overlaying": "y",
            "side": "right",
        },
    )
    return figure


@ui.refreshable
def governance_panel() -> None:
    summary = STATE.get("summary", {})
    last_refresh = summary.get("last_refresh")
    if last_refresh is not None and not pd.isna(last_refresh):
        refresh_display = pd.Timestamp(last_refresh).strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        refresh_display = "n/a"

    with ui.card().classes("w-full bg-[#161b22] border-l-4 border-[#ff7b72] p-4"):
        ui.label("Workbench Governance").classes("text-sm font-semibold text-[#e6edf3]")
        ui.markdown(
            f"""
- **Data source:** `{summary.get('data_source', 'none')}`
- **Records:** {summary.get('record_count', 0)}
- **Alerts:** {summary.get('alert_count', 0)}
- **System state:** **{summary.get('system_state', 'NOMINAL')}**
- **Last refresh:** {refresh_display}
- **Posture:** Local-first / High-trust
- **Store:** `{DEFAULT_DB_PATH.name}`
- **Test status:** pytest ingestion + duckdb + export suite
"""
        )


@ui.refreshable
def metrics_row() -> None:
    summary = STATE.get("summary", {})
    df = STATE.get("scored_df", pd.DataFrame())
    state = summary.get("system_state", "NOMINAL")
    state_color = "#ff7b72" if state == "DEGRADED" else "#3fb950"
    current_temp = float(df["temperature"].iloc[-1]) if not df.empty else 0.0
    battery = float(df["battery_level"].iloc[-1]) if not df.empty else 0.0

    with ui.row().classes("w-full gap-3"):
        with ui.column().classes("flex-1"):
            _metric_card("System State", state, f"Alerts: {summary.get('alert_count', 0)}", state_color)
        with ui.column().classes("flex-1"):
            _metric_card(
                "Core Temperature",
                f"{current_temp:.1f} °C",
                f"Warn > {TEMP_WARNING_THRESHOLD:.0f} °C | Crit > {TEMP_CRITICAL_THRESHOLD:.0f} °C",
            )
        with ui.column().classes("flex-1"):
            _metric_card(
                "Max Risk Index",
                f"{summary.get('max_risk_score', 0)} / 100",
                "Threshold: < 50",
                "#f0883e",
            )
        with ui.column().classes("flex-1"):
            _metric_card("Battery Level", f"{battery:.1f} %", "Source: PowerGrid-B")


@ui.refreshable
def telemetry_panel() -> None:
    df = STATE.get("scored_df", pd.DataFrame())
    if df.empty:
        ui.label("No telemetry loaded.").classes("text-[#8b949e]")
        return

    ui.plotly(_build_timeline_figure(df)).classes("w-full")

    conn = connect(DEFAULT_DB_PATH)
    try:
        alerts = fetch_alerts(conn)
    finally:
        conn.close()

    ui.label("Critical Alerts Queue").classes("text-sm font-semibold mt-4")
    if alerts.empty:
        ui.label("All systems nominal. No alerts active.").classes("text-[#3fb950]")
    else:
        rows = []
        for _, row in alerts.iterrows():
            rows.append(
                {
                    "timestamp": pd.Timestamp(row["timestamp"]).strftime("%Y-%m-%d %H:%M:%S"),
                    "cpu_utilization": f"{row['cpu_utilization']:.1f}",
                    "temperature": f"{row['temperature']:.1f}",
                    "risk_score": int(row["risk_score"]),
                }
            )
        ui.table(
            columns=[
                {"name": "timestamp", "label": "Timestamp", "field": "timestamp", "align": "left"},
                {"name": "cpu_utilization", "label": "CPU %", "field": "cpu_utilization"},
                {"name": "temperature", "label": "Temp °C", "field": "temperature"},
                {"name": "risk_score", "label": "Risk", "field": "risk_score"},
            ],
            rows=rows,
            row_key="timestamp",
        ).classes("w-full")


@ui.refreshable
def operator_log_table() -> None:
    log = _load_operator_log()
    if log is None or log.empty:
        ui.label("No operator actions logged yet.").classes("text-[#8b949e]")
        return
    rows = log.sort_values("timestamp", ascending=False).to_dict(orient="records")
    ui.table(
        columns=[
            {"name": "timestamp", "label": "Timestamp", "field": "timestamp", "align": "left"},
            {"name": "operator", "label": "Operator", "field": "operator"},
            {"name": "disposition", "label": "Disposition", "field": "disposition"},
            {"name": "action", "label": "Action", "field": "action", "align": "left"},
        ],
        rows=rows,
        row_key="timestamp",
    ).classes("w-full")


def operator_log_panel() -> None:
    operator = ui.input("Operator", value="Operator-01").classes("w-full")
    asset_id = ui.input("Asset ID", value="Asset-Sim-01").classes("w-full")
    action = ui.textarea("Action taken").classes("w-full")
    disposition = ui.select(
        ["Observed", "Mitigated", "Escalated", "Deferred"],
        value="Observed",
        label="Disposition",
    ).classes("w-full")

    def append_action() -> None:
        if not action.value or not action.value.strip():
            ui.notify("Action taken is required.", type="negative")
            return
        ACTION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry = pd.DataFrame(
            [
                {
                    "timestamp": pd.Timestamp.now(tz=timezone.utc)
                    .isoformat(timespec="seconds")
                    .replace("+00:00", "Z"),
                    "operator": operator.value,
                    "asset_id": asset_id.value,
                    "disposition": disposition.value,
                    "action": action.value.strip(),
                }
            ]
        )
        write_header = not ACTION_LOG_PATH.exists()
        entry.to_csv(ACTION_LOG_PATH, mode="a", header=write_header, index=False)
        action.value = ""
        ui.notify("Action appended to operator log.", type="positive")
        operator_log_table.refresh()

    ui.button("Append Action", on_click=append_action).props("color=primary")
    operator_log_table()

    def export_rca() -> None:
        df = STATE.get("scored_df", pd.DataFrame())
        if df.empty:
            ui.notify("Load telemetry before exporting RCA.", type="warning")
            return
        packet = build_rca_packet(df, STATE["data_source"], operator_log=_load_operator_log())
        paths = write_rca_exports(packet, EXPORT_DIR)
        ui.download(json.dumps(packet, indent=2), "rca_packet.json")
        ui.download(format_rca_markdown(packet), "rca_packet.md")
        ui.notify(f"RCA exported to {paths['json']}", type="positive")

    ui.button("Generate RCA Export", on_click=export_rca).props("outline color=orange")


@ui.refreshable
def degraded_mode_panel() -> None:
    summary = STATE.get("summary", {})
    degraded = STATE.get("degraded_mode", False)
    ui.switch(
        "Degraded mode (50% throttle)",
        value=degraded,
        on_change=lambda e: STATE.update({"degraded_mode": e.value}),
    )
    if summary.get("system_state") == "DEGRADED":
        ui.markdown(
            """
**Degraded-mode guidance**
- Reduce compute duty cycle to 50% until temperature and CPU return below thresholds.
- Verify cooling path and terminate orphan high-CPU processes.
- Continue logging operator actions for engineering handoff.
"""
        ).classes("text-sm text-[#8b949e]")
    else:
        ui.label("System nominal — degraded mode not required.").classes("text-[#3fb950] text-sm")


def _refresh_views() -> None:
    governance_panel.refresh()
    metrics_row.refresh()
    telemetry_panel.refresh()
    degraded_mode_panel.refresh()


@ui.page("/")
def mission_console() -> None:
    ui.dark_mode().enable()
    ui.add_head_html(
        """
        <style>
          body { background: #0f1115; }
          .nicegui-content { background: #0f1115; }
        </style>
        """
    )

    upload_state: dict[str, bytes | str] = {"bytes": b"", "name": ""}

    with ui.header().classes("bg-[#161b22] text-[#e6edf3] px-4 py-3"):
        ui.label("Mission Autonomy Field Support Console").classes("text-lg font-semibold")
        ui.label("NiceGUI + DuckDB | Operator-grade diagnostics").classes("text-xs text-[#8b949e]")

    with ui.row().classes("w-full gap-4 p-4 items-start"):
        with ui.column().classes("w-80 gap-3"):
            governance_panel()

            source_mode = ui.select(
                {
                    "mock": "Mock (synthetic)",
                    "fixture": "Fixture (sample_telemetry.csv)",
                    "upload": "Upload CSV",
                },
                value="fixture",
                label="Telemetry source",
            ).classes("w-full")

            upload = ui.upload(
                label="Telemetry CSV",
                auto_upload=True,
                on_upload=lambda e: upload_state.update(
                    {"bytes": e.content.read(), "name": e.name}
                ),
            ).classes("w-full")
            upload.set_visibility(source_mode.value == "upload")

            def on_source_change() -> None:
                upload.set_visibility(source_mode.value == "upload")

            source_mode.on_value_change(on_source_change)

            def ingest_clicked() -> None:
                mode_map = {
                    "mock": "Mock (synthetic)",
                    "fixture": "Fixture (sample_telemetry.csv)",
                    "upload": "Upload CSV",
                }
                _ingest_source(
                    mode_map[source_mode.value],
                    upload_bytes=upload_state.get("bytes") or None,
                    upload_name=str(upload_state.get("name") or ""),
                )
                _refresh_views()

            ui.button("Ingest telemetry", on_click=ingest_clicked).props("color=primary").classes(
                "w-full"
            )
            degraded_mode_panel()

        with ui.column().classes("flex-grow gap-4"):
            metrics_row()
            with ui.tabs().classes("w-full") as tabs:
                telemetry_tab = ui.tab("Telemetry & Alerts")
                log_tab = ui.tab("Operator Log")
                assist_tab = ui.tab("Assist / Briefs")
            with ui.tab_panels(tabs, value=telemetry_tab).classes("w-full"):
                with ui.tab_panel(telemetry_tab):
                    telemetry_panel()
                with ui.tab_panel(log_tab):
                    operator_log_panel()
                with ui.tab_panel(assist_tab):
                    ui.markdown(
                        """
**Prompt export mode**

Use ChatGPT/Codex/Grok/Claude briefs from `prompts/` with the current alert context.
Live API calls are intentionally not wired in this console.

**Offline checklist**
1. Verify cooling fan power lines.
2. Terminate orphan high-CPU threads.
3. Enable degraded mode if temperature remains above warning band.
4. Export RCA packet after operator actions are logged.
"""
                    ).classes("text-sm text-[#8b949e]")


def _bootstrap_default_fixture() -> None:
    _ingest_source("Fixture (sample_telemetry.csv)")


if __name__ in {"__main__", "__mp_main__"}:
    _bootstrap_default_fixture()
    ui.run(
        title="Mission Autonomy Field Support Console",
        host="127.0.0.1",
        port=8080,
        reload=False,
        dark=True,
    )