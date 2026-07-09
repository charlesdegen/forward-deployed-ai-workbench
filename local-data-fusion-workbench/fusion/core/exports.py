"""Export fused datasets and lineage artifacts."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import polars as pl

ARTIFACT_ROOT = Path(__file__).resolve().parents[2]
EXPORT_DIR = ARTIFACT_ROOT / "artifacts" / "exports"


def export_fused_dataset(
    df: pl.DataFrame,
    *,
    basename: str = "fused_dataset",
    export_dir: Path | None = None,
) -> dict[str, str]:
    target = export_dir or EXPORT_DIR
    target.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stem = f"{basename}_{stamp}"

    csv_path = target / f"{stem}.csv"
    parquet_path = target / f"{stem}.parquet"
    df.write_csv(csv_path)
    df.write_parquet(parquet_path)
    return {"csv": str(csv_path), "parquet": str(parquet_path)}


def export_lineage_markdown(content: str, *, basename: str = "fusion_lineage") -> str:
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = EXPORT_DIR / f"{basename}_{stamp}.md"
    path.write_text(content, encoding="utf-8")
    return str(path)