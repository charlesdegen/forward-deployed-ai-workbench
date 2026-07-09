"""Dataset profiling for operator-facing fusion decisions."""

from __future__ import annotations

from typing import Any

import polars as pl


def _null_percent(series: pl.Series) -> float:
    if series.len() == 0:
        return 0.0
    return round(float(series.null_count()) / series.len() * 100, 2)


def profile_column(name: str, series: pl.Series) -> dict[str, Any]:
    profile: dict[str, Any] = {
        "name": name,
        "dtype": str(series.dtype),
        "null_percent": _null_percent(series),
        "unique_count": int(series.n_unique()),
    }
    if series.dtype.is_numeric():
        profile.update(
            {
                "min": float(series.min()) if series.min() is not None else None,
                "max": float(series.max()) if series.max() is not None else None,
                "mean": float(series.mean()) if series.mean() is not None else None,
            }
        )
    else:
        samples = series.drop_nulls().unique().head(3).to_list()
        profile["sample_values"] = [str(value) for value in samples]
    return profile


def profile_frame(df: pl.DataFrame, dataset_name: str) -> dict[str, Any]:
    return {
        "dataset_name": dataset_name,
        "row_count": df.height,
        "column_count": df.width,
        "columns": [profile_column(name, df[name]) for name in df.columns],
    }