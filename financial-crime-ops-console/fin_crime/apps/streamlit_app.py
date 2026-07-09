"""Financial Crime Operations Console — Streamlit case workflow."""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st

ARTIFACT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTIFACT_ROOT))

from fin_crime.core.duckdb_store import (  # noqa: E402
    append_audit,
    connect,
    fetch_audit,
    fetch_cases,
    replace_cases,
)
from fin_crime.core.exports import build_evidence_packet, write_evidence_exports  # noqa: E402
from fin_crime.core.ingestion import load_transactions_csv, parse_transactions_csv  # noqa: E402
from fin_crime.core.scoring import case_queue, score_transactions  # noqa: E402

FIXTURE = ARTIFACT_ROOT / "fixtures" / "sample_transactions.csv"
DB_PATH = ARTIFACT_ROOT / "artifacts" / "fin_crime.duckdb"
EXPORT_DIR = ARTIFACT_ROOT / "artifacts" / "exports"

st.set_page_config(
    page_title="Financial Crime Operations Console",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Financial Crime Operations Console")
st.caption("Portfolio artifact #3 · Synthetic AML case triage · Local DuckDB audit trail")

with st.sidebar:
    st.header("Data source")
    source_mode = st.radio(
        "Input",
        ["Fixture (sample_transactions.csv)", "Upload CSV"],
        index=0,
    )
    uploaded = None
    if source_mode.startswith("Upload"):
        uploaded = st.file_uploader("Transaction CSV", type=["csv"])

    st.divider()
    st.header("Governance")
    st.markdown(
        """
        - **Data:** synthetic fixtures only  
        - **Scoring:** rule-based (no ML)  
        - **Exports:** training drafts, not filings  
        - **Skill:** `skills/fin-crime-skill/`
        """
    )
    last_refresh = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    st.caption(f"Last refresh: {last_refresh}")


def _load(source_mode: str, uploaded) -> tuple[pd.DataFrame, str]:
    if source_mode.startswith("Fixture"):
        return load_transactions_csv(FIXTURE), "fixtures/sample_transactions.csv"
    if uploaded is None:
        st.warning("Upload a CSV or select the fixture.")
        st.stop()
    return parse_transactions_csv(uploaded), f"upload:{uploaded.name}"


raw_df, data_source = _load(source_mode, uploaded)
scored = score_transactions(raw_df)
queue = case_queue(scored, min_score=25)

con = connect(DB_PATH)
replace_cases(con, scored)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Transactions", len(scored))
c2.metric("Case queue", len(queue))
c3.metric("Critical", int((scored["risk_band"] == "CRITICAL").sum()))
c4.metric("High", int((scored["risk_band"] == "HIGH").sum()))

tab_queue, tab_case, tab_audit, tab_export = st.tabs(
    ["Case queue", "Case workbench", "Audit trail", "Evidence export"]
)

with tab_queue:
    st.subheader("Open cases (risk ≥ 25)")
    st.dataframe(
        queue[
            [
                "transaction_id",
                "timestamp",
                "account_id",
                "amount_usd",
                "channel",
                "country_origin",
                "country_dest",
                "risk_score",
                "risk_band",
                "risk_flags",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

with tab_case:
    st.subheader("Case workbench")
    if queue.empty:
        st.info("No cases above threshold.")
    else:
        ids = queue["transaction_id"].tolist()
        selected = st.selectbox("Select case", ids)
        row = scored[scored["transaction_id"] == selected].iloc[0]
        st.json({k: (v.isoformat() if hasattr(v, "isoformat") else v) for k, v in row.to_dict().items()})

        actor = st.text_input("Actor", value=os.getenv("USER", "analyst"))
        action = st.selectbox(
            "Action",
            ["REVIEWED", "REQUEST_INFO", "ESCALATE", "CLOSE_FALSE_POSITIVE", "PREPARE_SAR_DRAFT"],
        )
        note = st.text_area("Note", value="")
        if st.button("Append audit event"):
            append_audit(
                con,
                transaction_id=selected,
                actor=actor,
                action=action,
                note=note,
                event_ts=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
            st.success(f"Logged {action} on {selected}")

with tab_audit:
    st.subheader("Audit trail")
    audit = fetch_audit(con)
    if audit.empty:
        st.caption("No audit events yet — use Case workbench.")
    else:
        st.dataframe(audit, use_container_width=True, hide_index=True)

with tab_export:
    st.subheader("Evidence packet export")
    st.warning("SAR narrative is a **training draft only** — not a regulatory filing.")
    export_ids = scored["transaction_id"].tolist()
    export_id = st.selectbox("Case to export", export_ids, key="export_id")
    if st.button("Write evidence packet"):
        case_row = scored[scored["transaction_id"] == export_id].iloc[0]
        packet = build_evidence_packet(case_row, fetch_audit(con), data_source=data_source)
        json_path, md_path = write_evidence_exports(packet, EXPORT_DIR)
        st.success(f"Wrote `{json_path.name}` and `{md_path.name}`")
        st.code(packet["sar_narrative_draft"])

st.divider()
st.caption(
    f"Source: `{data_source}` · DuckDB: `{DB_PATH.name}` · Offline · "
    f"Cases in store: {len(fetch_cases(con))}"
)
