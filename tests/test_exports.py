import json
import os

import jsonschema
import pandas as pd
import pytest

from src.core.exports import (
    build_rca_packet,
    format_rca_markdown,
    load_schema,
    write_rca_exports,
)
from src.core.ingestion import generate_mock_telemetry, load_telemetry_csv, score_anomalies


def _scored_row_dict(row: pd.Series) -> dict:
    payload = row.to_dict()
    payload["timestamp"] = pd.Timestamp(payload["timestamp"]).strftime("%Y-%m-%dT%H:%M:%S")
    payload["risk_score"] = int(payload["risk_score"])
    for flag in (
        "cpu_anomaly",
        "temp_warning",
        "temp_critical",
        "temp_anomaly",
        "sensor_anomaly",
        "comms_anomaly",
    ):
        payload[flag] = bool(payload[flag])
    return payload


def test_build_rca_packet_from_fixture():
    fixture_path = os.path.join(os.path.dirname(__file__), "..", "fixtures", "sample_telemetry.csv")
    scored = score_anomalies(load_telemetry_csv(fixture_path))
    packet = build_rca_packet(scored, "fixtures/sample_telemetry.csv")

    assert packet["governance"]["system_state"] == "DEGRADED"
    assert packet["governance"]["alert_count"] == 13
    assert packet["primary_finding"] is not None
    assert packet["primary_finding"]["risk_score"] == 100
    assert len(packet["recommendations"]) >= 1


def test_comms_alert_produces_comms_recommendation():
    """The comms recommendation branch in exports must be reachable from real scored data."""
    fixture_path = os.path.join(os.path.dirname(__file__), "..", "fixtures", "sample_telemetry.csv")
    scored = score_anomalies(load_telemetry_csv(fixture_path))
    packet = build_rca_packet(scored, "fixtures/sample_telemetry.csv")

    assert packet["primary_finding"]["flags"]["comms_anomaly"] is True
    assert any("antenna alignment" in rec for rec in packet["recommendations"])


def test_rca_packet_validates_against_schema():
    scored = score_anomalies(generate_mock_telemetry(50))
    packet = build_rca_packet(scored, "simulated_telemetry_v1")
    schema = load_schema("rca_packet_schema.json")
    jsonschema.validate(packet, schema)


def test_scored_row_validates_against_output_schema():
    scored = score_anomalies(generate_mock_telemetry(10))
    row = _scored_row_dict(scored.iloc[3])
    schema = load_schema("output_schema.json")
    jsonschema.validate(row, schema)


def test_input_row_validates_against_input_schema():
    df = generate_mock_telemetry(3)
    row = df.iloc[0].to_dict()
    row["timestamp"] = pd.Timestamp(row["timestamp"]).strftime("%Y-%m-%dT%H:%M:%S")
    schema = load_schema("input_schema.json")
    jsonschema.validate(row, schema)


def _valid_input_row() -> dict:
    df = generate_mock_telemetry(3)
    row = df.iloc[0].to_dict()
    row["timestamp"] = pd.Timestamp(row["timestamp"]).strftime("%Y-%m-%dT%H:%M:%S")
    return row


@pytest.mark.parametrize(
    "field, bad_value",
    [
        ("battery_level", 150.0),
        ("battery_level", -1.0),
        ("cpu_utilization", 101.0),
        ("sensor_drift", -0.1),
        ("comms_link", 120.0),
    ],
)
def test_input_schema_rejects_out_of_range_values(field, bad_value):
    """The published bounds must actually bind, not merely be documented."""
    row = _valid_input_row()
    row[field] = bad_value
    schema = load_schema("input_schema.json")

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(row, schema)


def test_input_schema_rejects_missing_required_column():
    row = _valid_input_row()
    del row["comms_link"]
    schema = load_schema("input_schema.json")

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(row, schema)


def test_output_schema_rejects_risk_score_above_maximum():
    scored = score_anomalies(generate_mock_telemetry(10))
    row = _scored_row_dict(scored.iloc[3])
    row["risk_score"] = 101
    schema = load_schema("output_schema.json")

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(row, schema)


def test_rca_packet_schema_rejects_negative_alert_count():
    scored = score_anomalies(generate_mock_telemetry(50))
    packet = build_rca_packet(scored, "simulated_telemetry_v1")
    packet["governance"]["alert_count"] = -1
    schema = load_schema("rca_packet_schema.json")

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(packet, schema)


def test_write_rca_exports_creates_json_and_markdown(tmp_path):
    scored = score_anomalies(generate_mock_telemetry(20))
    packet = build_rca_packet(scored, "simulated_telemetry_v1")
    paths = write_rca_exports(packet, tmp_path, basename="test_rca")

    assert os.path.exists(paths["json"])
    assert os.path.exists(paths["markdown"])

    with open(paths["json"], encoding="utf-8") as handle:
        loaded = json.load(handle)
    assert loaded["governance"]["data_source"] == "simulated_telemetry_v1"

    markdown = open(paths["markdown"], encoding="utf-8").read()
    assert "# RCA Packet" in markdown
    assert "simulated_telemetry_v1" in markdown


def test_format_rca_markdown_includes_operator_actions():
    scored = score_anomalies(generate_mock_telemetry(5))
    operator_log = pd.DataFrame([
        {
            "timestamp": "2026-07-08T12:00:00Z",
            "operator": "Operator-01",
            "asset_id": "Asset-1",
            "disposition": "Observed",
            "action": "Checked cooling fan.",
        }
    ])
    packet = build_rca_packet(scored, "mock", operator_log=operator_log)
    markdown = format_rca_markdown(packet)

    assert "Checked cooling fan" in markdown
    assert "Operator actions" in markdown