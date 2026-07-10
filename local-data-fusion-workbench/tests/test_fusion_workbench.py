import os
import sys
from pathlib import Path

import pytest

ARTIFACT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ARTIFACT_ROOT))

from fusion.core.anomalies import build_anomaly_report  # noqa: E402
from fusion.core.duckdb_store import connect, fetch_table, register_dataset, register_fused  # noqa: E402
from fusion.core.exports import export_fused_dataset, export_lineage_markdown  # noqa: E402
from fusion.core.fusion import fuse_datasets  # noqa: E402
from fusion.core.ingestion import load_dataset  # noqa: E402
from fusion.core.lineage import build_mermaid_lineage  # noqa: E402
from fusion.core.matching import add_normalized_key, join_coverage, normalize_key, suggest_join_keys  # noqa: E402
from fusion.core.profiling import profile_frame  # noqa: E402

FIXTURES = ARTIFACT_ROOT / "fixtures"


@pytest.fixture
def customers_and_transactions():
    customers, _ = load_dataset(FIXTURES / "customers.csv")
    transactions, _ = load_dataset(FIXTURES / "transactions.csv")
    return customers, transactions


def test_load_fixture_bundle(customers_and_transactions):
    customers, transactions = customers_and_transactions
    assert customers.height == 4
    assert transactions.height == 8


def test_profile_frame(customers_and_transactions):
    customers, _ = customers_and_transactions
    profile = profile_frame(customers, "customers.csv")
    assert profile["row_count"] == 4
    assert profile["column_count"] == 4
    assert profile["columns"][0]["name"] == "customer_id"


def test_suggest_join_keys(customers_and_transactions):
    customers, transactions = customers_and_transactions
    suggestions = suggest_join_keys(customers, transactions)
    assert suggestions
    assert suggestions[0]["left_key"] == "customer_id"


def test_fuse_customers_transactions(customers_and_transactions):
    customers, transactions = customers_and_transactions
    fused = fuse_datasets(
        transactions,
        customers,
        left_key="customer_id",
        right_key="customer_id",
        how="left",
    )
    assert fused.height == 8
    assert "amount" in fused.columns
    assert "segment" in fused.columns


def test_orphan_keys_detected(customers_and_transactions):
    customers, transactions = customers_and_transactions
    fused = fuse_datasets(
        transactions,
        customers,
        left_key="customer_id",
        right_key="customer_id",
        how="left",
    )
    report = build_anomaly_report(
        transactions,
        customers,
        fused,
        left_key="customer_id",
        right_key="customer_id",
        numeric_column="amount",
    )
    orphans = report["orphan_keys"]
    assert "C999" in orphans["orphan_keys_in_left"]
    assert "C888" in orphans["orphan_keys_in_left"]
    assert "C004" in orphans["orphan_keys_in_right"]


def test_join_coverage(customers_and_transactions):
    customers, transactions = customers_and_transactions
    coverage = join_coverage(customers, transactions, "customer_id", "customer_id")
    assert coverage["matched_keys"] == 3
    assert coverage["right_only_keys"] == 2


def test_duckdb_register_and_fetch(customers_and_transactions, tmp_path):
    customers, transactions = customers_and_transactions
    fused = fuse_datasets(
        transactions,
        customers,
        left_key="customer_id",
        right_key="customer_id",
        how="left",
    )
    conn = connect(tmp_path / "fusion.duckdb")
    try:
        register_dataset(conn, "customers", customers)
        register_dataset(conn, "transactions", transactions)
        register_fused(conn, fused)
        loaded = fetch_table(conn, "fused_output")
        assert loaded.height == 8
    finally:
        conn.close()


def test_export_fused_and_lineage(customers_and_transactions, tmp_path):
    customers, transactions = customers_and_transactions
    fused = fuse_datasets(
        transactions,
        customers,
        left_key="customer_id",
        right_key="customer_id",
        how="left",
    )
    paths = export_fused_dataset(fused, export_dir=tmp_path)
    assert os.path.exists(paths["csv"])
    assert os.path.exists(paths["parquet"])

    lineage = build_mermaid_lineage(
        sources=[
            {"name": "customers.csv", "rows": "4"},
            {"name": "transactions.csv", "rows": "8"},
        ],
        join_spec={"how": "left", "left_key": "customer_id", "right_key": "customer_id"},
        output_name="fused_customer_transactions",
    )
    lineage_path = export_lineage_markdown(lineage, basename="test_lineage")
    assert Path(lineage_path).exists()
    assert "flowchart LR" in Path(lineage_path).read_text(encoding="utf-8")

def test_normalize_key_strips_case_punctuation_and_whitespace():
    assert normalize_key("  Acme, Inc. ") == "acmeinc"
    assert normalize_key("ACME-001") == "acme001"
    assert normalize_key(42) == "42"
    assert normalize_key("") == ""


def test_add_normalized_key_default_and_custom_column(customers_and_transactions):
    customers, _ = customers_and_transactions
    defaulted = add_normalized_key(customers, "customer_id")
    assert "customer_id__normalized" in defaulted.columns

    named = add_normalized_key(customers, "customer_id", output_column="entity_key")
    assert "entity_key" in named.columns
    assert named["entity_key"].to_list() == [normalize_key(v) for v in customers["customer_id"].to_list()]


def test_load_dataset_json_and_parquet_paths(customers_and_transactions, tmp_path):
    customers, _ = customers_and_transactions

    json_path = tmp_path / "customers.json"
    json_path.write_text(customers.write_json(), encoding="utf-8")
    from_json, label = load_dataset(json_path)
    assert from_json.height == customers.height
    assert label == "customers.json"

    parquet_path = tmp_path / "customers.parquet"
    customers.write_parquet(parquet_path)
    from_parquet, _ = load_dataset(parquet_path)
    assert from_parquet.height == customers.height


def test_load_dataset_excel_path(customers_and_transactions, tmp_path):
    customers, _ = customers_and_transactions
    xlsx_path = tmp_path / "customers.xlsx"
    customers.to_pandas().to_excel(xlsx_path, index=False)
    from_excel, _ = load_dataset(xlsx_path)
    assert from_excel.height == customers.height
    assert set(from_excel.columns) == set(customers.columns)


def test_load_dataset_rejects_unsupported_extension(tmp_path):
    bad = tmp_path / "notes.txt"
    bad.write_text("not tabular", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported file type"):
        load_dataset(bad)


def test_load_dataset_filelike_json_array_and_csv():
    from io import BytesIO

    json_frame, label = load_dataset(BytesIO(b'[{"customer_id": "C001", "amount": 10}]'))
    assert json_frame.height == 1
    assert label == "uploaded_dataset"

    csv_frame, _ = load_dataset(BytesIO(b"customer_id,amount\nC001,10\n"), name="upload.csv")
    assert csv_frame.height == 1


def test_load_dataset_filelike_rejects_json_object_and_empty_upload():
    from io import BytesIO

    with pytest.raises(ValueError, match="array of records"):
        load_dataset(BytesIO(b'{"customer_id": "C001"}'))
    # polars parses almost any text as single-column CSV; an empty upload is
    # the reliable trigger for the CSV fallback's error path.
    with pytest.raises(ValueError, match="CSV or JSON"):
        load_dataset(BytesIO(b""))


def test_fuse_inner_outer_cross_joins(customers_and_transactions):
    customers, transactions = customers_and_transactions

    inner = fuse_datasets(transactions, customers, left_key="customer_id", right_key="customer_id", how="inner")
    assert inner.height == 6  # C999/C888 orphan transactions drop

    outer = fuse_datasets(transactions, customers, left_key="customer_id", right_key="customer_id", how="outer")
    assert outer.height == 9  # 8 transactions + unmatched customer C004

    cross = fuse_datasets(transactions, customers, left_key="customer_id", right_key="customer_id", how="cross")
    assert cross.height == transactions.height * customers.height


def test_fuse_with_distinct_key_names(customers_and_transactions):
    customers, transactions = customers_and_transactions
    renamed = customers.rename({"customer_id": "entity_id"})
    fused = fuse_datasets(transactions, renamed, left_key="customer_id", right_key="entity_id", how="inner")
    assert fused.height == 6
    assert "segment" in fused.columns


def test_fuse_rejects_unknown_join_type(customers_and_transactions):
    customers, transactions = customers_and_transactions
    with pytest.raises(ValueError, match="Unsupported join type"):
        fuse_datasets(transactions, customers, left_key="customer_id", right_key="customer_id", how="semi")


def test_governance_panel_state_records_source_and_refresh():
    """Governance visibility: the fusion surface must name its source and refresh time."""
    from fusion.apps.nicegui_app import STATE, _load_fixture_bundle

    assert STATE["data_source"] == "none"
    assert STATE["last_refresh"] == "never"

    _load_fixture_bundle()

    assert "customers.csv" in STATE["data_source"]
    assert STATE["last_refresh"].endswith("Z")
    assert STATE["last_refresh"] != "never"
