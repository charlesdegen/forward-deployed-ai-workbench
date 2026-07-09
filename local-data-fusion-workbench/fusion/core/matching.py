"""Entity key normalization and join candidate detection."""

from __future__ import annotations

import re

import polars as pl


def normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value).strip().lower())


def add_normalized_key(df: pl.DataFrame, column: str, output_column: str | None = None) -> pl.DataFrame:
    target = output_column or f"{column}__normalized"
    return df.with_columns(
        pl.col(column).cast(pl.Utf8).map_elements(normalize_key, return_dtype=pl.Utf8).alias(target)
    )


def suggest_join_keys(left: pl.DataFrame, right: pl.DataFrame) -> list[dict[str, str]]:
    suggestions: list[dict[str, str]] = []
    for left_col in left.columns:
        for right_col in right.columns:
            if left_col.lower() == right_col.lower():
                suggestions.append(
                    {
                        "left_key": left_col,
                        "right_key": right_col,
                        "reason": "exact column name match",
                    }
                )
            elif left_col.lower().endswith("_id") and right_col.lower().endswith("_id"):
                if left_col.lower().replace("_id", "") == right_col.lower().replace("_id", ""):
                    suggestions.append(
                        {
                            "left_key": left_col,
                            "right_key": right_col,
                            "reason": "shared entity id stem",
                        }
                    )
    if not suggestions and "customer_id" in left.columns and "customer_id" in right.columns:
        suggestions.append(
            {
                "left_key": "customer_id",
                "right_key": "customer_id",
                "reason": "default customer entity key",
            }
        )
    return suggestions


def join_coverage(
    left: pl.DataFrame,
    right: pl.DataFrame,
    left_key: str,
    right_key: str,
) -> dict[str, int | float]:
    left_keys = set(left[left_key].cast(pl.Utf8).to_list())
    right_keys = set(right[right_key].cast(pl.Utf8).to_list())
    matched = left_keys & right_keys
    return {
        "left_unique_keys": len(left_keys),
        "right_unique_keys": len(right_keys),
        "matched_keys": len(matched),
        "left_only_keys": len(left_keys - right_keys),
        "right_only_keys": len(right_keys - left_keys),
        "match_rate_left": round(len(matched) / len(left_keys) * 100, 2) if left_keys else 0.0,
        "match_rate_right": round(len(matched) / len(right_keys) * 100, 2) if right_keys else 0.0,
    }