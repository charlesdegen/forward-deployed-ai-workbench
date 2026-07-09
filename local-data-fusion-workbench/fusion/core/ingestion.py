"""Load local tabular datasets for fusion workflows."""

from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path

import polars as pl


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json", ".parquet"}


def load_dataset(source: str | Path | BytesIO, *, name: str | None = None) -> tuple[pl.DataFrame, str]:
    """Load a dataset from path or file-like object. Returns frame and display name."""
    if isinstance(source, (str, Path)):
        path = Path(source)
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        label = name or path.name
        if path.suffix.lower() == ".csv":
            return pl.read_csv(path), label
        if path.suffix.lower() in {".xlsx", ".xls"}:
            import pandas as pd

            return pl.from_pandas(pd.read_excel(path)), label
        if path.suffix.lower() == ".json":
            return pl.read_json(path), label
        return pl.read_parquet(path), label

    label = name or "uploaded_dataset"
    head = source.read(2048)
    source.seek(0)
    if head.strip().startswith(b"{") or head.strip().startswith(b"["):
        payload = json.load(source)
        if isinstance(payload, list):
            return pl.DataFrame(payload), label
        raise ValueError("JSON must be an array of records for fusion ingest")

    try:
        return pl.read_csv(source), label
    except Exception as exc:
        raise ValueError("Upload must be CSV or JSON array") from exc