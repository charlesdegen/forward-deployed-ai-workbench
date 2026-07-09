"""Local Data Fusion Workbench — NiceGUI + Polars + DuckDB."""

from __future__ import annotations

import json
import sys
from io import BytesIO
from pathlib import Path

from nicegui import ui

ARTIFACT_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = ARTIFACT_ROOT / "fixtures"
sys.path.insert(0, str(ARTIFACT_ROOT))

from fusion.core.anomalies import build_anomaly_report  # noqa: E402
from fusion.core.duckdb_store import connect, register_dataset, register_fused  # noqa: E402
from fusion.core.exports import export_fused_dataset, export_lineage_markdown  # noqa: E402
from fusion.core.fusion import fuse_datasets  # noqa: E402
from fusion.core.ingestion import load_dataset  # noqa: E402
from fusion.core.lineage import build_mermaid_lineage  # noqa: E402
from fusion.core.matching import join_coverage, suggest_join_keys  # noqa: E402
from fusion.core.profiling import profile_frame  # noqa: E402

STATE: dict = {
    "datasets": {},
    "profiles": {},
    "fused": None,
    "anomalies": {},
    "lineage": "",
    "join_spec": {"how": "left", "left_key": "customer_id", "right_key": "customer_id"},
    "export_paths": {},
}


def _dataset_names() -> list[str]:
    return list(STATE["datasets"].keys())


def _load_fixture_bundle() -> None:
    customers, customers_name = load_dataset(FIXTURES_DIR / "customers.csv")
    transactions, transactions_name = load_dataset(FIXTURES_DIR / "transactions.csv")
    events, events_name = load_dataset(FIXTURES_DIR / "events.json")

    STATE["datasets"] = {
        transactions_name: transactions,
        customers_name: customers,
        events_name: events,
    }
    STATE["profiles"] = {
        name: profile_frame(frame, name) for name, frame in STATE["datasets"].items()
    }
    suggestions = suggest_join_keys(customers, transactions)
    if suggestions:
        STATE["join_spec"].update(suggestions[0])


def _persist_to_duckdb() -> None:
    conn = connect()
    try:
        for name, frame in STATE["datasets"].items():
            register_dataset(conn, name.replace(".", "_"), frame)
        if STATE["fused"] is not None:
            register_fused(conn, STATE["fused"])
    finally:
        conn.close()


@ui.refreshable
def governance_panel() -> None:
    names = _dataset_names()
    fused_rows = STATE["fused"].height if STATE["fused"] is not None else 0
    ui.markdown(
        f"""
**Fusion Governance**
- Datasets loaded: `{len(names)}`
- DuckDB store: `artifacts/data_fusion.duckdb`
- Fused rows: `{fused_rows}`
- Posture: Local-first / High-trust
- Test status: `pytest: data fusion suite`
"""
    )


@ui.refreshable
def profile_panel() -> None:
    if not STATE["profiles"]:
        ui.label("Load fixtures or upload datasets to profile.").classes("text-[#8b949e]")
        return
    for profile in STATE["profiles"].values():
        with ui.expansion(f"{profile['dataset_name']} ({profile['row_count']} rows)", icon="table_chart").classes(
            "w-full"
        ):
            rows = [
                {
                    "column": column["name"],
                    "dtype": column["dtype"],
                    "null_%": column["null_percent"],
                    "unique": column["unique_count"],
                }
                for column in profile["columns"]
            ]
            ui.table(
                columns=[
                    {"name": "column", "label": "Column", "field": "column", "align": "left"},
                    {"name": "dtype", "label": "Type", "field": "dtype"},
                    {"name": "null_%", "label": "Null %", "field": "null_%"},
                    {"name": "unique", "label": "Unique", "field": "unique"},
                ],
                rows=rows,
                row_key="column",
            ).classes("w-full")


@ui.refreshable
def fusion_controls() -> None:
    names = _dataset_names()
    if len(names) < 2:
        ui.label("Need at least two datasets to fuse.").classes("text-[#8b949e]")
        return

    left_name = ui.select(names, label="Left dataset", value=names[0]).classes("w-full")
    right_name = ui.select(names, label="Right dataset", value=names[1] if len(names) > 1 else names[0]).classes(
        "w-full"
    )
    how = ui.select(["left", "inner", "outer"], value=STATE["join_spec"]["how"], label="Join type").classes("w-full")

    left_df = STATE["datasets"][left_name.value]
    right_df = STATE["datasets"][right_name.value]
    suggestions = suggest_join_keys(left_df, right_df)
    default_left = suggestions[0]["left_key"] if suggestions else left_df.columns[0]
    default_right = suggestions[0]["right_key"] if suggestions else right_df.columns[0]

    left_key = ui.select(left_df.columns, label="Left key", value=default_left).classes("w-full")
    right_key = ui.select(right_df.columns, label="Right key", value=default_right).classes("w-full")

    coverage = join_coverage(left_df, right_df, left_key.value, right_key.value)
    ui.markdown(
        f"""
**Join coverage**
- Matched keys: {coverage['matched_keys']}
- Orphan keys (right): {coverage['right_only_keys']}
- Match rate (right): {coverage['match_rate_right']}%
"""
    )

    def run_fusion() -> None:
        fused = fuse_datasets(
            left_df,
            right_df,
            left_key=left_key.value,
            right_key=right_key.value,
            how=how.value,
        )
        numeric_column = "amount" if "amount" in fused.columns else None
        anomalies = build_anomaly_report(
            left_df,
            right_df,
            fused,
            left_key=left_key.value,
            right_key=right_key.value,
            numeric_column=numeric_column,
        )
        lineage = build_mermaid_lineage(
            sources=[
                {"name": left_name.value, "rows": str(left_df.height)},
                {"name": right_name.value, "rows": str(right_df.height)},
            ],
            join_spec={
                "how": how.value,
                "left_key": left_key.value,
                "right_key": right_key.value,
            },
            output_name="fused_customer_transactions",
            anomalies=anomalies,
        )
        STATE["fused"] = fused
        STATE["anomalies"] = anomalies
        STATE["lineage"] = lineage
        STATE["join_spec"] = {
            "how": how.value,
            "left_key": left_key.value,
            "right_key": right_key.value,
        }
        _persist_to_duckdb()
        fused_panel.refresh()
        anomaly_panel.refresh()
        lineage_panel.refresh()
        governance_panel.refresh()
        ui.notify(f"Fused dataset created ({fused.height} rows).", type="positive")

    ui.button("Run fusion", on_click=run_fusion).props("color=primary").classes("w-full")


@ui.refreshable
def fused_panel() -> None:
    fused = STATE.get("fused")
    if fused is None:
        ui.label("No fused dataset yet.").classes("text-[#8b949e]")
        return
    preview = fused.head(20).to_dicts()
    columns = [{"name": col, "label": col, "field": col, "align": "left"} for col in fused.columns]
    ui.table(columns=columns, rows=preview, row_key=fused.columns[0]).classes("w-full")


@ui.refreshable
def anomaly_panel() -> None:
    anomalies = STATE.get("anomalies") or {}
    if not anomalies:
        ui.label("Run fusion to generate anomaly report.").classes("text-[#8b949e]")
        return
    orphans = anomalies.get("orphan_keys", {})
    ui.markdown(
        f"""
**Orphan keys**
- In right dataset: `{', '.join(orphans.get('orphan_keys_in_right', [])[:10]) or 'none'}`
- In left dataset: `{', '.join(orphans.get('orphan_keys_in_left', [])[:10]) or 'none'}`

**Duplicate keys**
- Left: {len(anomalies.get('duplicate_left_keys', []))}
- Right: {len(anomalies.get('duplicate_right_keys', []))}
"""
    )


@ui.refreshable
def lineage_panel() -> None:
    lineage = STATE.get("lineage", "")
    if not lineage:
        ui.label("Fusion lineage diagram will appear here.").classes("text-[#8b949e]")
        return
    ui.markdown(lineage)

    def export_all() -> None:
        fused = STATE.get("fused")
        if fused is None:
            ui.notify("Run fusion before export.", type="warning")
            return
        paths = export_fused_dataset(fused, basename="fused_customer_transactions")
        lineage_path = export_lineage_markdown(
            "# Fusion Lineage\n\n" + lineage + "\n\n## Anomalies\n\n```json\n"
            + json.dumps(STATE.get("anomalies", {}), indent=2)
            + "\n```\n"
        )
        STATE["export_paths"] = {**paths, "lineage": lineage_path}
        ui.download(fused.to_pandas().to_csv(index=False).encode("utf-8"), "fused_preview.csv")
        ui.notify(f"Exported CSV, Parquet, and lineage to artifacts/exports/", type="positive")

    ui.button("Export fused dataset + lineage", on_click=export_all).props("outline color=orange")


@ui.page("/")
def fusion_workbench() -> None:
    ui.dark_mode().enable()
    ui.add_head_html("<style>body,.nicegui-content{background:#0f1115;}</style>")

    with ui.header().classes("bg-[#161b22] text-[#e6edf3] px-4 py-3"):
        ui.label("Local Data Fusion Workbench").classes("text-lg font-semibold")
        ui.label("Polars + DuckDB | Upload · Profile · Join · Detect · Export").classes("text-xs text-[#8b949e]")

    with ui.row().classes("w-full gap-4 p-4 items-start"):
        with ui.column().classes("w-80 gap-3"):
            governance_panel()
            ui.button("Load fixture bundle", on_click=lambda: (_load_fixture_bundle(), profile_panel.refresh(), fusion_controls.refresh(), governance_panel.refresh(), ui.notify("Fixtures loaded.", type="positive"))).props("color=primary").classes("w-full")

            upload_state: dict = {"bytes": b"", "name": ""}

            def on_upload(event) -> None:
                upload_state["bytes"] = event.content.read()
                upload_state["name"] = event.name

            ui.upload(label="Upload CSV/JSON", auto_upload=True, on_upload=on_upload).classes("w-full")

            def ingest_upload() -> None:
                if not upload_state["bytes"]:
                    ui.notify("Choose a file first.", type="warning")
                    return
                frame, label = load_dataset(BytesIO(upload_state["bytes"]), name=upload_state["name"])
                STATE["datasets"][label] = frame
                STATE["profiles"][label] = profile_frame(frame, label)
                _persist_to_duckdb()
                profile_panel.refresh()
                fusion_controls.refresh()
                governance_panel.refresh()
                ui.notify(f"Ingested {label} ({frame.height} rows).", type="positive")

            ui.button("Ingest upload", on_click=ingest_upload).classes("w-full")
            fusion_controls()

        with ui.column().classes("flex-grow gap-3"):
            with ui.tabs().classes("w-full") as tabs:
                profile_tab = ui.tab("Profile")
                fused_tab = ui.tab("Fused preview")
                anomaly_tab = ui.tab("Anomalies")
                lineage_tab = ui.tab("Lineage & Export")
            with ui.tab_panels(tabs, value=profile_tab).classes("w-full"):
                with ui.tab_panel(profile_tab):
                    profile_panel()
                with ui.tab_panel(fused_tab):
                    fused_panel()
                with ui.tab_panel(anomaly_tab):
                    anomaly_panel()
                with ui.tab_panel(lineage_tab):
                    lineage_panel()


if __name__ in {"__main__", "__mp_main__"}:
    _load_fixture_bundle()
    ui.run(title="Local Data Fusion Workbench", host="127.0.0.1", port=8081, reload=False, dark=True)