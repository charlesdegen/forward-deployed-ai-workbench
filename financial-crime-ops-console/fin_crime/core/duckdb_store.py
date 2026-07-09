"""Local DuckDB persistence for scored cases and audit events."""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd


def connect(db_path: str | Path) -> duckdb.DuckDBPyConnection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(path))
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS cases (
            transaction_id VARCHAR PRIMARY KEY,
            timestamp TIMESTAMP,
            account_id VARCHAR,
            amount_usd DOUBLE,
            risk_score INTEGER,
            risk_band VARCHAR,
            risk_flags VARCHAR,
            case_status VARCHAR,
            channel VARCHAR,
            country_origin VARCHAR,
            country_dest VARCHAR
        )
        """
    )
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_log (
            event_id INTEGER,
            event_ts TIMESTAMP,
            transaction_id VARCHAR,
            actor VARCHAR,
            action VARCHAR,
            note VARCHAR
        )
        """
    )
    return con


def replace_cases(con: duckdb.DuckDBPyConnection, scored: pd.DataFrame) -> None:
    subset = scored[
        [
            "transaction_id",
            "timestamp",
            "account_id",
            "amount_usd",
            "risk_score",
            "risk_band",
            "risk_flags",
            "case_status",
            "channel",
            "country_origin",
            "country_dest",
        ]
    ]
    con.execute("DELETE FROM cases")
    con.register("_cases_df", subset)
    con.execute("INSERT INTO cases SELECT * FROM _cases_df")
    con.unregister("_cases_df")


def append_audit(
    con: duckdb.DuckDBPyConnection,
    transaction_id: str,
    actor: str,
    action: str,
    note: str,
    event_ts: str,
) -> None:
    row = con.execute("SELECT COALESCE(MAX(event_id), 0) + 1 FROM audit_log").fetchone()
    event_id = int(row[0]) if row else 1
    con.execute(
        "INSERT INTO audit_log VALUES (?, ?, ?, ?, ?, ?)",
        [event_id, event_ts, transaction_id, actor, action, note],
    )


def fetch_cases(con: duckdb.DuckDBPyConnection, min_score: int = 0) -> pd.DataFrame:
    return con.execute(
        "SELECT * FROM cases WHERE risk_score >= ? ORDER BY risk_score DESC",
        [min_score],
    ).df()


def fetch_audit(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    return con.execute("SELECT * FROM audit_log ORDER BY event_id").df()
