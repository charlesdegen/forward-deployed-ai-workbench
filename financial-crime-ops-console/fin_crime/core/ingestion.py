"""Load synthetic financial transaction alerts for case triage."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "transaction_id",
    "timestamp",
    "account_id",
    "counterparty_id",
    "amount_usd",
    "currency",
    "channel",
    "country_origin",
    "country_dest",
    "is_cross_border",
    "customer_segment",
    "prior_sar_count",
}


def validate_transaction_schema(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required transaction columns: {', '.join(sorted(missing))}")


def load_transactions_csv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    validate_transaction_schema(df)
    return df


def parse_transactions_csv(source) -> pd.DataFrame:
    df = pd.read_csv(source, parse_dates=["timestamp"])
    validate_transaction_schema(df)
    return df
