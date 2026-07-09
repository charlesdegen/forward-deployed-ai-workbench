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

    if left_key == right_key:
        return left.join(right, on=left_key, how=how, suffix=suffix)
    return left.join(right, left_on=left_key, right_on=right_key, how=how, suffix=suffix)