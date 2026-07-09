import os

import pytest

from src.core.duckdb_store import (
    connect,
    fetch_active_session,
    fetch_alerts,
    fetch_scored_telemetry,
    fetch_summary,
    init_schema,
    store_scored_telemetry,
)
from src.core.ingestion import load_telemetry_csv, score_anomalies


@pytest.fixture
def fixture_scored():
    path = os.path.join(os.path.dirname(__file__), "..", "fixtures", "sample_telemetry.csv")
    return score_anomalies(load_telemetry_csv(path))


def test_init_schema_is_idempotent(tmp_path):
    conn = connect(tmp_path / "test.duckdb")
    try:
        init_schema(conn)
        init_schema(conn)
        tables = {row[0] for row in conn.execute("SHOW TABLES").fetchall()}
        assert "telemetry_scored" in tables
        assert "ingest_sessions" in tables
    finally:
        conn.close()


def test_store_and_query_scored_telemetry(tmp_path, fixture_scored):
    db_path = tmp_path / "mission.duckdb"
    conn = connect(db_path)
    try:
        session_id = store_scored_telemetry(conn, fixture_scored, "fixtures/sample_telemetry.csv")
        assert len(session_id) == 12

        session = fetch_active_session(conn)
        assert session is not None
        assert session["data_source"] == "fixtures/sample_telemetry.csv"
        assert session["record_count"] == 50
        assert session["system_state"] == "DEGRADED"
        assert session["alert_count"] == 13

        scored = fetch_scored_telemetry(conn)
        assert len(scored) == 50
        assert int(scored["risk_score"].max()) == 100

        alerts = fetch_alerts(conn)
        assert len(alerts) == 13

        summary = fetch_summary(conn)
        assert summary["max_risk_score"] == 100
        assert summary["min_battery"] > 0
    finally:
        conn.close()


def test_comms_anomaly_round_trips_through_duckdb(tmp_path, fixture_scored):
    """The SQL layer must preserve the comms flag, not just the Python scoring."""
    conn = connect(tmp_path / "mission.duckdb")
    try:
        store_scored_telemetry(conn, fixture_scored, "fixtures/sample_telemetry.csv")
        comms_rows = conn.execute(
            "SELECT row_index, risk_score FROM telemetry_scored WHERE comms_anomaly ORDER BY row_index"
        ).fetchall()

        assert [row[0] for row in comms_rows] == [40, 41, 42, 45]
        # Row 41 is comms-only, so its risk is exactly the comms weight.
        assert dict(comms_rows)[41] == 20
    finally:
        conn.close()


def test_replace_session_on_reingest(tmp_path, fixture_scored):
    conn = connect(tmp_path / "mission.duckdb")
    try:
        first = store_scored_telemetry(conn, fixture_scored, "source-a")
        second = store_scored_telemetry(conn, fixture_scored.iloc[:10], "source-b")

        assert first != second
        session = fetch_active_session(conn)
        assert session["data_source"] == "source-b"
        assert session["record_count"] == 10
        assert len(fetch_scored_telemetry(conn)) == 10
    finally:
        conn.close()