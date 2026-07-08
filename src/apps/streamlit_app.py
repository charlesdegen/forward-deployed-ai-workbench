import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, timezone

# Adjust path to find core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.core.ingestion import (
    TEMP_CRITICAL_THRESHOLD,
    TEMP_WARNING_THRESHOLD,
    generate_mock_telemetry,
    load_telemetry_csv,
    parse_telemetry_csv,
    score_anomalies,
)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
DEFAULT_FIXTURE_PATH = os.path.join(REPO_ROOT, 'fixtures/sample_telemetry.csv')
ACTION_LOG_PATH = os.path.join(REPO_ROOT, 'artifacts/operator_action_log.csv')

# Page configuration
st.set_page_config(
    page_title="Mission Autonomy Field Support Console",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme CSS overrides
st.markdown("""
<style>
    .reportview-container {
        background: #0f1115;
    }
    .metric-card {
        background-color: #171a21;
        border: 1px solid #232733;
        border-radius: 4px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
    }
    .metric-label {
        font-size: 12px;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-sub {
        font-size: 10px;
        color: #484f58;
        margin-top: 4px;
    }
    .gov-panel {
        background-color: #161b22;
        border-left: 3px solid #ff7b72;
        padding: 10px;
        margin-top: 15px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# App Title & Header
st.title("🛰️ Mission Autonomy Field Support Console")
st.caption("Forward-Deployed AI Systems Workbench | Operator-Grade Diagnostics")

with st.sidebar:
    st.header("📡 Telemetry Source")
    source_mode = st.radio(
        "Data input",
        ["Mock (synthetic)", "Fixture (sample_telemetry.csv)", "Upload CSV"],
        index=1,
    )
    uploaded_file = None
    if source_mode == "Upload CSV":
        uploaded_file = st.file_uploader("Telemetry CSV", type=["csv"])

    st.divider()
    st.header("🤖 Triage Agent Setup")
    api_key = st.text_input("OPENAI_API_KEY", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    st.info("Prompt export mode: ChatGPT frames diagnostic reasoning and Codex keeps the repo, tests, and repair loop reproducible.")


def load_telemetry(source_mode: str, uploaded_file) -> tuple[pd.DataFrame, str]:
    if source_mode == "Mock (synthetic)":
        return generate_mock_telemetry(num_records=50), "simulated_telemetry_v1"
    if source_mode == "Fixture (sample_telemetry.csv)":
        return load_telemetry_csv(DEFAULT_FIXTURE_PATH), "fixtures/sample_telemetry.csv"
    if uploaded_file is None:
        st.warning("Upload a telemetry CSV or choose another data source.")
        st.stop()
    try:
        return parse_telemetry_csv(uploaded_file), uploaded_file.name
    except ValueError as exc:
        st.error(f"Telemetry schema validation failed: {exc}")
        st.stop()


df, data_source_label = load_telemetry(source_mode, uploaded_file)
scored_df = score_anomalies(df)

last_refresh = scored_df["timestamp"].max()
if pd.isna(last_refresh):
    last_refresh_display = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
else:
    last_refresh_display = pd.Timestamp(last_refresh).strftime("%Y-%m-%dT%H:%M:%SZ")

alert_count = int((scored_df["risk_score"] > 0).sum())
system_state = "DEGRADED" if alert_count > 0 else "NOMINAL"
state_color = "#ff7b72" if alert_count > 0 else "#3fb950"

with st.sidebar:
    st.header("⚙️ Workbench Governance")
    st.markdown(f"""
    **Metadata Attributes:**
    - **Data Source**: `{data_source_label}`
    - **Record Count**: `{len(scored_df)}`
    - **Sensor Freq**: `1 Hz (assumed)`
    - **Last Refresh**: `{last_refresh_display}`
    - **Deployment Posture**: Local-First / High-Trust
    - **Test Status**: `pytest: ingestion suite`
    - **Operator Owner**: FDE-Team-01
    """)

# Top Metric Panel
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">System State</div>
        <div class="metric-value" style="color: {state_color};">{system_state}</div>
        <div class="metric-sub">Source: {data_source_label} | Alerts: {alert_count}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    current_temp = scored_df['temperature'].iloc[-1]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Core Temperature</div>
        <div class="metric-value">{current_temp:.1f} °C</div>
        <div class="metric-sub">Warning: > {TEMP_WARNING_THRESHOLD:.1f} °C | Critical: > {TEMP_CRITICAL_THRESHOLD:.1f} °C</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    max_risk = scored_df['risk_score'].max()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Max Risk Index</div>
        <div class="metric-value" style="color: #f0883e;">{max_risk} / 100</div>
        <div class="metric-sub">Source: Scoring Engine | Threshold: < 50</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    battery = scored_df['battery_level'].iloc[-1]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Battery Level</div>
        <div class="metric-value">{battery:.1f} %</div>
        <div class="metric-sub">Source: PowerGrid-B | Rate: -0.1%/s</div>
    </div>
    """, unsafe_allow_html=True)

# Main Data View and Visualizations
tab_data, tab_log, tab_ai = st.tabs(["📊 Telemetry & Alerts", "🧾 Operator Log", "🤖 ChatGPT / Codex Assistant"])

with tab_data:
    col_chart, col_table = st.columns([2, 1])

    with col_chart:
        st.subheader("Sensor Telemetry Timelines")
        st.line_chart(scored_df.set_index('timestamp')[['cpu_utilization', 'temperature', 'battery_level']])

    with col_table:
        st.subheader("Critical Alerts Queue")
        alerts = scored_df[scored_df['risk_score'] > 0][['timestamp', 'cpu_utilization', 'temperature', 'risk_score']]
        if not alerts.empty:
            st.dataframe(
                alerts.sort_values(by='timestamp', ascending=False),
                column_config={
                    "timestamp": "Timestamp",
                    "cpu_utilization": st.column_config.NumberColumn("CPU %", format="%.1f"),
                    "temperature": st.column_config.NumberColumn("Temp °C", format="%.1f"),
                    "risk_score": st.column_config.ProgressColumn("Risk", min_value=0, max_value=100, format="%d")
                },
                hide_index=True
            )
        else:
            st.success("All systems nominal. No alerts active.")

with tab_log:
    st.subheader("Operator Action Log")
    st.write("Actions are appended locally for RCA packets and engineering handoff.")

    with st.form("operator_action_form", clear_on_submit=True):
        operator = st.text_input("Operator", value="Operator-01")
        asset_id = st.text_input("Asset ID", value="Asset-Sim-01")
        action = st.text_area("Action taken", placeholder="Describe the diagnostic action, observation, or handoff note.")
        disposition = st.selectbox("Disposition", ["Observed", "Mitigated", "Escalated", "Deferred"])
        submitted = st.form_submit_button("Append Action")

    if submitted:
        if action.strip():
            os.makedirs(os.path.dirname(ACTION_LOG_PATH), exist_ok=True)
            entry = pd.DataFrame([
                {
                    "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
                    "operator": operator,
                    "asset_id": asset_id,
                    "disposition": disposition,
                    "action": action.strip(),
                }
            ])
            write_header = not os.path.exists(ACTION_LOG_PATH)
            entry.to_csv(ACTION_LOG_PATH, mode="a", header=write_header, index=False)
            st.success(f"Action appended to {ACTION_LOG_PATH}")
        else:
            st.error("Action taken is required before appending to the log.")

    if os.path.exists(ACTION_LOG_PATH):
        action_log = pd.read_csv(ACTION_LOG_PATH)
        st.dataframe(action_log.sort_values(by="timestamp", ascending=False), hide_index=True)
    else:
        st.info("No operator actions logged yet.")

with tab_ai:
    st.subheader("ChatGPT / Codex Triage Loop")
    st.write("This starter exports high-context prompts. Use ChatGPT to draft diagnostic reasoning from the alert context, then use Codex to implement repairs, tests, and export improvements in this repository.")

    if not api_key:
        st.warning("No `OPENAI_API_KEY` detected. Prompt export still works offline; live API calls are intentionally not wired in this starter.")

        st.subheader("Offline Fallback Triage Checklist")
        st.markdown("""
        **Alert Detected**: CPU & Temperature Spikes (>85% CPU, >80°C warning, >85°C critical)

        **Recommended Checklist:**
        1.  [ ] Verify cooling fan power lines.
        2.  [ ] Terminate orphan compute threads (e.g. `kill -9` on high CPU loads).
        3.  [ ] Switch system operation to Degraded Mode (50% throttle).
        4.  [ ] Check for thermal throttling sensor logs.
        """)
    else:
        st.success("API key detected. This starter still runs in prompt export mode; use the generated brief as the payload for ChatGPT or Codex.")

        critical_telemetry = scored_df[scored_df['risk_score'] > 0].to_dict(orient='records')

        st.subheader("ChatGPT Diagnostic Prompt")
        st.code(
            f"""You are supporting a field operator triaging autonomous asset telemetry.

Use the triage priorities from skills/triage-skill/SKILL.md:
1. Safety and power
2. Communications
3. Sensor alignment
4. Compute and software

Data source: {data_source_label}
Anomalous telemetry records:
{critical_telemetry}

Return:
- likely primary failing component
- telemetry values that triggered the finding
- operator-safe checklist
- assumptions and uncertainty
- engineering feedback packet
""",
            language="text",
        )

        st.subheader("Codex Repair Brief")
        st.code(
            """Inspect the telemetry scoring and Streamlit app.
Add or repair tests for the observed failure mode.
Keep scoring logic in src/core and UI changes in src/apps.
Run pytest and summarize changed files, verification output, and remaining risks.""",
            language="text",
        )