"""Local DuckDB persistence for Mission Autonomy telemetry and alert queries."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "artifacts" / "mission_console.duckdb"

SCORED_COLUMNS = [
    "timestamp",
    "battery_level",
    "cpu_utilization",
    "sensor_drift",
    "comms_link",
    "temperature",
    "cpu_anomaly",
    "temp_warning",
    "temp_critical",
    "temp_anomaly",
    "sensor_anomaly",
    "comms_anomaly",
    "risk_score",
]


def connect(db_path: str | Path = DEFAULT_DB_PATH) -> duckdb.DuckDBPyConnection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(path))


def init_schema(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ingest_sessions (
            session_id VARCHAR PRIMARY KEY,
            data_source VARCHAR NOT NULL,
            ingested_at TIMESTAMP NOT NULL,
            record_count INTEGER NOT NULL,
            system_state VARCHAR NOT NULL,
            alert_count INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS telemetry_scored (
            session_id VARCHAR NOT NULL,
            row_index INTEGER NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            battery_level DOUBLE NOT NULL,
            cpu_utilization DOUBLE NOT NULL,
            sensor_drift DOUBLE NOT NULL,
            comms_link DOUBLE NOT NULL,
            temperature DOUBLE NOT NULL,
            cpu_anomaly BOOLEAN NOT NULL,
            temp_warning BOOLEAN NOT NULL,
            temp_critical BOOLEAN NOT NULL,
            temp_anomaly BOOLEAN NOT NULL,
            sensor_anomaly BOOLEAN NOT NULL,
            comms_anomaly BOOLEAN NOT NULL,
            risk_score INTEGER NOT NULL
        );
        """
    )


def _prepare_scored_frame(scored_df: pd.DataFrame) -> pd.DataFrame:
    frame = scored_df.reset_index(drop=True).copy()
    frame["row_index"] = frame.index
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    for column in (
        "cpu_anomaly",
        "temp_warning",
        "temp_critical",
        "temp_anomaly",
        "sensor_anomaly",
        "comms_anomaly",
    ):
        frame[column] = frame[column].astype(bool)
    frame["risk_score"] = frame["risk_score"].astype(int)
    return frame


def store_scored_telemetry(
    conn: duckdb.DuckDBPyConnection,
    scored_df: pd.DataFrame,
    data_source: str,
) -> str:
    """Replace active telemetry with a newly scored frame. Returns session_id."""
    init_schema(conn)
    prepared = _prepare_scored_frame(scored_df)
    alert_count = int((prepared["risk_score"] > 0).sum())
    system_state = "DEGRADED" if alert_count > 0 else "NOMINAL"
    session_id = uuid.uuid4().hex[:12]
    ingested_at = datetime.now(timezone.utc).replace(tzinfo=None)

    conn.execute("DELETE FROM telemetry_scored")
    conn.execute("DELETE FROM ingest_sessions")

    conn.execute(
        """
        INSERT INTO ingest_sessions (
            session_id, data_source, ingested_at, record_count, system_state, alert_count
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        [session_id, data_source, ingested_at, len(prepared), system_state, alert_count],
    )

    prepared["session_id"] = session_id
    conn.register("prepared_scored", prepared)
    conn.execute(
        """
        INSERT INTO telemetry_scored (
            session_id, row_index, timestamp, battery_level, cpu_utilization,
            sensor_drift, comms_link, temperature, cpu_anomaly, temp_warning,
            temp_critical, temp_anomaly, sensor_anomaly, comms_anomaly, risk_score
        )
        SELECT
            session_id, row_index, timestamp, battery_level, cpu_utilization,
            sensor_drift, comms_link, temperature, cpu_anomaly, temp_warning,
            temp_critical, temp_anomaly, sensor_anomaly, comms_anomaly, risk_score
        FROM prepared_scored
        """
    )
    conn.unregister("prepared_scored")
    return session_id


def fetch_active_session(conn: duckdb.DuckDBPyConnection) -> dict | None:
    init_schema(conn)
    row = conn.execute(
        """
        SELECT session_id, data_source, ingested_at, record_count, system_state, alert_count
        FROM ingest_sessions
        ORDER BY ingested_at DESC
        LIMIT 1
        """
    ).fetchone()
    if row is None:
        return None
    keys = (
        "session_id",
        "data_source",
        "ingested_at",
        "record_count",
        "system_state",
        "alert_count",
    )
    return dict(zip(keys, row, strict=True))


def fetch_scored_telemetry(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    init_schema(conn)
    frame = conn.execute(
        """
        SELECT
            timestamp, battery_level, cpu_utilization, sensor_drift, comms_link,
            temperature, cpu_anomaly, temp_warning, temp_critical, temp_anomaly,
            sensor_anomaly, comms_anomaly, risk_score
        FROM telemetry_scored
        ORDER BY row_index
        """
    ).df()
    if frame.empty:
        return frame
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    return frame


def fetch_alerts(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    init_schema(conn)
    return conn.execute(
        """
        SELECT timestamp, cpu_utilization, temperature, risk_score
        FROM telemetry_scored
        WHERE risk_score > 0
        ORDER BY timestamp DESC
        """
    ).df()


def fetch_summary(conn: duckdb.DuckDBPyConnection) -> dict:
    session = fetch_active_session(conn)
    if session is None:
        return {
            "data_source": "none",
            "record_count": 0,
            "alert_count": 0,
            "system_state": "NOMINAL",
            "max_risk_score": 0,
            "last_refresh": None,
        }

    stats = conn.execute(
        """
        SELECT
            MAX(timestamp) AS last_refresh,
            MAX(risk_score) AS max_risk_score,
            AVG(cpu_utilization) AS avg_cpu,
            AVG(temperature) AS avg_temp,
            MIN(battery_level) AS min_battery
        FROM telemetry_scored
        """
    ).fetchone()

    last_refresh, max_risk, avg_cpu, avg_temp, min_battery = stats
    return {
        **session,
        "last_refresh": last_refresh,
        "max_risk_score": int(max_risk or 0),
        "avg_cpu": float(avg_cpu or 0.0),
        "avg_temp": float(avg_temp or 0.0),
        "min_battery": float(min_battery or 0.0),
    }