"""Dataset join and fusion operations."""

from __future__ import annotations

import polars as pl

JOIN_TYPES = {"left", "inner", "outer", "cross"}


def fuse_datasets(
    left: pl.DataFrame,
    right: pl.DataFrame,
    *,
    left_key: str,
    right_key: str,
    how: str = "left",
    suffix: str = "_right",
) -> pl.DataFrame:
    if how not in JOIN_TYPES:
        raise ValueError(f"Unsupported join type: {how}")

    if how == "cross":
        # A cross join is a cartesian product; polars rejects join keys for it.
        return left.join(right, how="cross", suffix=suffix)

    # Public API keeps "outer"; polars renamed it to "full".
    polars_how = "full" if how == "outer" else how
    if left_key == right_key:
        return left.join(right, on=left_key, how=polars_how, suffix=suffix)
    return left.join(right, left_on=left_key, right_on=right_key, how=polars_how, suffix=suffix)