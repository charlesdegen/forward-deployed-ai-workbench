"""LLM Red-Team Eval Harness — offline suite runner and report export."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st

ARTIFACT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTIFACT_ROOT))

from redteam.core.exports import build_report, write_report  # noqa: E402
from redteam.core.runner import run_suite  # noqa: E402
from redteam.core.scoring import summarize_results  # noqa: E402
from redteam.core.suite import load_suite  # noqa: E402

FIXTURE = ARTIFACT_ROOT / "fixtures" / "redteam_suite.json"
EXPORT_DIR = ARTIFACT_ROOT / "artifacts" / "exports"

st.set_page_config(page_title="LLM Red-Team Eval Harness", layout="wide")
st.title("LLM Red-Team Eval Harness")
st.caption("Portfolio artifact #4 · Offline heuristics · Fixture responses by default")

with st.sidebar:
    st.header("Governance")
    st.markdown(
        """
        - **Default:** fixture responses + pattern checks  
        - **Live models:** not called in this starter  
        - **Scorecard:** `evals/security_scorecard.md`  
        - **Skill:** `skills/redteam-skill/`
        """
    )
    st.caption(f"Refresh: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")

cases = load_suite(FIXTURE)
results = run_suite(cases)
summary = summarize_results(results)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Cases", summary["total"])
c2.metric("Passed", summary["passed"])
c3.metric("Failed", summary["failed"])
c4.metric("Security score", summary["security_score"], help=summary["band"])

st.info(f"Ship band: **{summary['band']}** · Pass rate {summary['pass_rate']}")

tab_results, tab_cat, tab_export = st.tabs(["Results", "By category", "Export report"])

with tab_results:
    df = pd.DataFrame(results)
    show = df[
        ["case_id", "category", "severity", "passed", "expected_behavior", "response_excerpt"]
    ]
    st.dataframe(show, use_container_width=True, hide_index=True)

with tab_cat:
    st.json(summary["by_category"])
    st.subheader("By severity")
    st.json(summary["by_severity"])

with tab_export:
    if st.button("Write red-team report"):
        report = build_report(results, summary)
        json_path, md_path = write_report(report, EXPORT_DIR)
        st.success(f"Wrote `{json_path.name}` and `{md_path.name}`")
        st.markdown(md_path.read_text(encoding="utf-8"))

st.divider()
st.caption(f"Source: `{FIXTURE.name}` · Offline · No live LLM calls")
