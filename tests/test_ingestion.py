import sys
import os

# Adjust path to find core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import pytest

from io import StringIO

from src.core.ingestion import (
    TEMP_CRITICAL_THRESHOLD,
    TEMP_WARNING_THRESHOLD,
    generate_mock_telemetry,
    load_telemetry_csv,
    parse_telemetry_csv,
    score_anomalies,
    validate_telemetry_schema,
)

def test_telemetry_generation():
    df = generate_mock_telemetry(num_records=10)
    assert len(df) == 10
    assert 'timestamp' in df.columns
    assert 'cpu_utilization' in df.columns
    assert 'temperature' in df.columns

def test_anomaly_scoring():
    df = generate_mock_telemetry(num_records=50)
    scored = score_anomalies(df)
    
    # Anomaly 1 should be caught (at index 30)
    assert scored.loc[30, 'cpu_anomaly']
    assert scored.loc[30, 'temp_anomaly']
    assert scored.loc[30, 'temperature'] > TEMP_CRITICAL_THRESHOLD
    assert scored.loc[30, 'temp_warning']
    assert scored.loc[30, 'temp_critical']
    assert scored.loc[30, 'risk_score'] > 0


def test_temperature_warning_below_critical():
    df = generate_mock_telemetry(num_records=5)
    df.loc[0, 'temperature'] = TEMP_WARNING_THRESHOLD + 1
    scored = score_anomalies(df)

    assert scored.loc[0, 'temp_warning']
    assert not scored.loc[0, 'temp_critical']


def test_validate_telemetry_schema_reports_missing_columns():
    df = pd.DataFrame({'timestamp': ['2026-07-08T00:00:00Z']})

    with pytest.raises(ValueError, match='battery_level'):
        validate_telemetry_schema(df)


def test_load_telemetry_csv_validates_schema(tmp_path):
    csv_path = tmp_path / 'telemetry.csv'
    generate_mock_telemetry(num_records=3).to_csv(csv_path, index=False)

    loaded = load_telemetry_csv(str(csv_path))

    assert len(loaded) == 3
    assert 'timestamp' in loaded.columns


def test_parse_telemetry_csv_accepts_file_like_object():
    buffer = StringIO()
    generate_mock_telemetry(num_records=4).to_csv(buffer, index=False)
    buffer.seek(0)

    loaded = parse_telemetry_csv(buffer)

    assert len(loaded) == 4
    assert 'battery_level' in loaded.columns


def test_fixture_sample_telemetry_loads():
    fixture_path = os.path.join(os.path.dirname(__file__), '..', 'fixtures', 'sample_telemetry.csv')
    loaded = load_telemetry_csv(fixture_path)
    scored = score_anomalies(loaded)

    assert len(loaded) == 50
    assert scored['risk_score'].max() > 0
