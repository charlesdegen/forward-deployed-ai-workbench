import streamlit as st
import pandas as pd
import sys
import os

# Adjust path to find core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.core.ingestion import generate_mock_telemetry, score_anomalies

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

# Governance Metadata Layer (surfaced as a first-class feature)
with st.sidebar:
    st.header("⚙️ Workbench Governance")
    st.markdown("""
    **Metadata Attributes:**
    - **Data Source**: `simulated_telemetry_v1.csv`
    - **Sensor Freq**: `1 Hz`
    - **Last Refresh**: `2026-07-08T04:00:00Z`
    - **Deployment Posture**: Local-First / High-Trust
    - **Operator Owner**: FDE-Team-01
    """)
    
    st.divider()
    
    st.header("🤖 Triage Agent Setup")
    api_key = st.text_input("OPENAI_API_KEY", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    
    st.info("ChatGPT frames diagnostic reasoning and Codex keeps the repo, tests, and repair loop reproducible.")

# Load and score telemetry data
df = generate_mock_telemetry(num_records=50)
scored_df = score_anomalies(df)

# Top Metric Panel
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">System State</div>
        <div class="metric-value" style="color: #ff7b72;">DEGRADED</div>
        <div class="metric-sub">Source: Telemetry scoring | Owner: Operator-01</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    current_temp = scored_df['temperature'].iloc[-1]
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Core Temperature</div>
        <div class="metric-value">{current_temp:.1f} °C</div>
        <div class="metric-sub">Source: Temp-Sensor-4 | Threshold: < 80.0 °C</div>
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
tab_data, tab_ai = st.tabs(["📊 Telemetry & Alerts", "🤖 ChatGPT / Codex Assistant"])

with tab_data:
    col_chart, col_table = st.columns([2, 1])
    
    with col_chart:
        st.subheader("Sensor Telemetry Timelines")
        # Line charts for metrics
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

with tab_ai:
    st.subheader("ChatGPT / Codex Triage Loop")
    st.write("Use ChatGPT to draft diagnostic reasoning from the alert context, then use Codex to implement repairs, tests, and export improvements in this repository.")
    
    if not api_key:
        st.warning("Configure `OPENAI_API_KEY` in the sidebar when you are ready to connect live OpenAI-backed assistant features.")
        
        # Fallback Mock Triage Instructions
        st.subheader("Offline Fallback Triage Checklist")
        st.markdown("""
        **Alert Detected**: CPU & Temperature Spikes (>85% CPU, >80°C Temp)
        
        **Recommended Checklist:**
        1.  [ ] Verify cooling fan power lines.
        2.  [ ] Terminate orphan compute threads (e.g. `kill -9` on high CPU loads).
        3.  [ ] Switch system operation to Degraded Mode (50% throttle).
        4.  [ ] Check for thermal throttling sensor logs.
        """)
    else:
        st.success("API key detected. Use the generated brief as the payload for a ChatGPT troubleshooting review or a Codex repair task.")

        critical_telemetry = scored_df[scored_df['risk_score'] > 0].to_dict(orient='records')

        st.subheader("ChatGPT Diagnostic Prompt")
        st.code(
            f"""You are supporting a field operator triaging autonomous asset telemetry.

Use the triage priorities from skills/triage-skill/SKILL.md:
1. Safety and power
2. Communications
3. Sensor alignment
4. Compute and software

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
