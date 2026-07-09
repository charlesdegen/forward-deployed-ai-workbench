"""DuckDB persistence for fusion datasets and SQL inspection."""

from __future__ import annotations

from pathlib import Path

import duckdb
import polars as pl

ARTIFACT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = ARTIFACT_ROOT / "artifacts" / "data_fusion.duckdb"


def connect(db_path: str | Path = DEFAULT_DB_PATH) -> duckdb.DuckDBPyConnection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(path))


def register_dataset(conn: duckdb.DuckDBPyConnection, name: str, df: pl.DataFrame) -> None:
    safe_name = name.replace("-", "_").replace(" ", "_")
    conn.register(safe_name, df.to_pandas())
    conn.execute(f"CREATE OR REPLACE TABLE {safe_name} AS SELECT * FROM {safe_name}")
    conn.unregister(safe_name)


def register_fused(conn: duckdb.DuckDBPyConnection, df: pl.DataFrame, table_name: str = "fused_output") -> None:
    register_dataset(conn, table_name, df)


def fetch_table(conn: duckdb.DuckDBPyConnection, table_name: str) -> pl.DataFrame:
    pandas_frame = conn.execute(f"SELECT * FROM {table_name}").df()
    return pl.from_pandas(pandas_frame)


def run_sql(conn: duckdb.DuckDBPyConnection, query: str) -> pl.DataFrame:
    return pl.from_pandas(conn.execute(query).df())