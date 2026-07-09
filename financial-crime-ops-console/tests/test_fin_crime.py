import io
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ARTIFACT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ARTIFACT_ROOT))

from fin_crime.core.duckdb_store import append_audit, connect, fetch_audit, replace_cases  # noqa: E402
from fin_crime.core.exports import build_evidence_packet, write_evidence_exports  # noqa: E402
from fin_crime.core.ingestion import (  # noqa: E402
    load_transactions_csv,
    parse_transactions_csv,
    validate_transaction_schema,
)
from fin_crime.core.scoring import (  # noqa: E402
    CASE_QUEUE_MIN_SCORE,
    case_queue,
    score_transactions,
)

FIXTURE = ARTIFACT_ROOT / "fixtures" / "sample_transactions.csv"
GOLDEN = ARTIFACT_ROOT / "tests" / "golden_outputs" / "fixture_case_summary.json"


def test_fixture_loads():
    df = load_transactions_csv(FIXTURE)
    assert len(df) == 12
    validate_transaction_schema(df)


def test_scoring_bands_and_critical_case():
    df = load_transactions_csv(FIXTURE)
    scored = score_transactions(df)
    assert "risk_score" in scored.columns
    critical = scored[scored["transaction_id"] == "TX-1007"].iloc[0]
    assert critical["risk_band"] == "CRITICAL"
    assert critical["risk_score"] >= 70
    queue = case_queue(scored)
    assert len(queue) >= 3
    assert queue.iloc[0]["risk_score"] >= queue.iloc[-1]["risk_score"]


def _fixture_case_summary() -> dict:
    scored = score_transactions(load_transactions_csv(FIXTURE))
    return {
        "record_count": int(len(scored)),
        "band_counts": {b: int(n) for b, n in sorted(scored["risk_band"].value_counts().items())},
        "queue_size": int(len(case_queue(scored))),
        "queue_order": case_queue(scored)["transaction_id"].tolist(),
        "cases": {
            row["transaction_id"]: {
                "risk_score": int(row["risk_score"]),
                "risk_band": row["risk_band"],
                "risk_flags": row["risk_flags"],
            }
            for _, row in scored.iterrows()
        },
    }


def test_fixture_scoring_matches_golden_summary():
    """Pins every score, band, and flag so a weight change cannot pass silently."""
    expected = json.loads(GOLDEN.read_text(encoding="utf-8"))
    assert _fixture_case_summary() == expected


def test_all_four_risk_bands_are_exercised_by_the_fixture():
    scored = score_transactions(load_transactions_csv(FIXTURE))
    assert set(scored["risk_band"]) == {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


def test_case_queue_uses_shared_min_score_constant():
    scored = score_transactions(load_transactions_csv(FIXTURE))
    queue = case_queue(scored)

    assert (queue["risk_score"] >= CASE_QUEUE_MIN_SCORE).all()
    assert len(queue) == int((scored["risk_score"] >= CASE_QUEUE_MIN_SCORE).sum())


def test_cross_border_false_row_is_not_flagged():
    scored = score_transactions(load_transactions_csv(FIXTURE))
    domestic = scored[~scored["is_cross_border"].astype(bool)]

    assert len(domestic) > 0
    assert not domestic["risk_flags"].str.contains("cross_border").any()


def test_parse_transactions_csv_accepts_file_like_object(tmp_path):
    raw = FIXTURE.read_bytes()
    buffer = io.BytesIO(raw)

    parsed = parse_transactions_csv(buffer)

    assert len(parsed) == 12
    validate_transaction_schema(parsed)


def test_schema_rejects_missing_columns():
    bad = pd.DataFrame({"transaction_id": ["X"]})
    with pytest.raises(ValueError, match="Missing required"):
        validate_transaction_schema(bad)


def test_duckdb_audit_and_cases(tmp_path):
    df = score_transactions(load_transactions_csv(FIXTURE))
    con = connect(tmp_path / "test.duckdb")
    replace_cases(con, df)
    append_audit(con, "TX-1007", "tester", "ESCALATE", "unit test", "2026-07-09T00:00:00Z")
    audit = fetch_audit(con)
    assert len(audit) == 1
    assert audit.iloc[0]["action"] == "ESCALATE"


def test_evidence_export(tmp_path):
    scored = score_transactions(load_transactions_csv(FIXTURE))
    row = scored[scored["transaction_id"] == "TX-1007"].iloc[0]
    packet = build_evidence_packet(row)
    assert packet["governance"]["synthetic_data"] is True
    assert "training" in packet["sar_narrative_draft"].lower() or "draft" in packet["sar_narrative_draft"].lower()
    json_path, md_path = write_evidence_exports(packet, tmp_path)
    assert json_path.exists()
    assert md_path.exists()
