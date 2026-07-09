"""Anomaly detection for fused and source datasets."""

from __future__ import annotations

from typing import Any

import polars as pl


def detect_duplicate_keys(df: pl.DataFrame, key_column: str) -> list[dict[str, Any]]:
    grouped = (
        df.group_by(key_column)
        .agg(pl.len().alias("row_count"))
        .filter(pl.col("row_count") > 1)
        .sort("row_count", descending=True)
    )
    return grouped.to_dicts()


def detect_orphan_keys(
    left: pl.DataFrame,
    right: pl.DataFrame,
    left_key: str,
    right_key: str,
) -> dict[str, list[str]]:
    left_keys = set(left[left_key].cast(pl.Utf8).to_list())
    right_keys = set(right[right_key].cast(pl.Utf8).to_list())
    return {
        "orphan_keys_in_right": sorted(right_keys - left_keys),
        "orphan_keys_in_left": sorted(left_keys - right_keys),
    }


def detect_numeric_outliers(df: pl.DataFrame, column: str) -> list[dict[str, Any]]:
    if column not in df.columns or not df[column].dtype.is_numeric():
        return []

    series = df[column].drop_nulls()
    if series.len() < 4:
        return []

    q1 = float(series.quantile(0.25))
    q3 = float(series.quantile(0.75))
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = df.filter((pl.col(column) < lower) | (pl.col(column) > upper))
    return outliers.select([column]).head(20).to_dicts()


def build_anomaly_report(
    left: pl.DataFrame,
    right: pl.DataFrame,
    fused: pl.DataFrame | None,
    *,
    left_key: str,
    right_key: str,
    numeric_column: str | None = None,
) -> dict[str, Any]:
    report: dict[str, Any] = {
        "orphan_keys": detect_orphan_keys(left, right, left_key, right_key),
        "duplicate_left_keys": detect_duplicate_keys(left, left_key),
        "duplicate_right_keys": detect_duplicate_keys(right, right_key),
        "numeric_outliers": [],
    }
    if fused is not None and numeric_column:
        report["numeric_outliers"] = detect_numeric_outliers(fused, numeric_column)
    return report