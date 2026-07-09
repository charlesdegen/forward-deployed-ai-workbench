import sys
from pathlib import Path

import pandas as pd
import pytest

ARTIFACT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ARTIFACT_ROOT))

from fin_crime.core.duckdb_store import append_audit, connect, fetch_audit, replace_cases  # noqa: E402
from fin_crime.core.exports import build_evidence_packet, write_evidence_exports  # noqa: E402
from fin_crime.core.ingestion import load_transactions_csv, validate_transaction_schema  # noqa: E402
from fin_crime.core.scoring import case_queue, score_transactions  # noqa: E402

FIXTURE = ARTIFACT_ROOT / "fixtures" / "sample_transactions.csv"


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
