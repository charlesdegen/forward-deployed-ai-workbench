import sys
import os

# Adjust path to find core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import pytest

from io import StringIO

from src.core.ingestion import (
    COMMS_LINK_THRESHOLD,
    TEMP_CRITICAL_THRESHOLD,
    TEMP_WARNING_THRESHOLD,
    derive_system_state,
    generate_mock_telemetry,
    load_telemetry_csv,
    parse_telemetry_csv,
    score_anomalies,
    summarize_alert_state,
    validate_telemetry_ranges,
    validate_telemetry_schema,
)


def _csv_buffer(df) -> StringIO:
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

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


def test_comms_anomaly_flags_and_weights_degraded_link():
    df = generate_mock_telemetry(num_records=5)
    df.loc[0, 'comms_link'] = COMMS_LINK_THRESHOLD - 1
    scored = score_anomalies(df)

    assert scored.loc[0, 'comms_anomaly']
    # Comms is the only tripped flag on this row, so risk equals its published weight.
    assert scored.loc[0, 'risk_score'] == 20
    assert not scored.loc[1, 'comms_anomaly']


def test_comms_link_at_threshold_is_not_an_anomaly():
    df = generate_mock_telemetry(num_records=5)
    df.loc[0, 'comms_link'] = COMMS_LINK_THRESHOLD
    scored = score_anomalies(df)

    assert not scored.loc[0, 'comms_anomaly']


def test_mock_generator_injects_comms_degradation():
    scored = score_anomalies(generate_mock_telemetry(num_records=50))

    assert scored.loc[20:22, 'comms_anomaly'].all()
    assert not scored.loc[25, 'comms_anomaly']


def test_summarize_alert_state_matches_scoring():
    nominal = score_anomalies(generate_mock_telemetry(num_records=5))
    assert summarize_alert_state(nominal) == {'alert_count': 0, 'system_state': 'NOMINAL'}

    degraded = score_anomalies(generate_mock_telemetry(num_records=50))
    state = summarize_alert_state(degraded)
    assert state['system_state'] == 'DEGRADED'
    assert state['alert_count'] == int((degraded['risk_score'] > 0).sum())


def test_derive_system_state_boundary():
    assert derive_system_state(0) == 'NOMINAL'
    assert derive_system_state(1) == 'DEGRADED'


def test_validate_telemetry_ranges_rejects_battery_above_maximum():
    df = generate_mock_telemetry(num_records=3)
    df.loc[0, 'battery_level'] = 150.0

    with pytest.raises(ValueError, match='battery_level'):
        validate_telemetry_ranges(df)


def test_validate_telemetry_ranges_rejects_negative_sensor_drift():
    df = generate_mock_telemetry(num_records=3)
    df.loc[0, 'sensor_drift'] = -5.0

    with pytest.raises(ValueError, match='sensor_drift'):
        validate_telemetry_ranges(df)


def test_validate_telemetry_ranges_accepts_fixture():
    fixture_path = os.path.join(os.path.dirname(__file__), '..', 'fixtures', 'sample_telemetry.csv')
    validate_telemetry_ranges(pd.read_csv(fixture_path))


def test_parse_telemetry_csv_rejects_out_of_range_values():
    df = generate_mock_telemetry(num_records=3)
    df.loc[1, 'cpu_utilization'] = 250.0

    with pytest.raises(ValueError, match='cpu_utilization'):
        parse_telemetry_csv(_csv_buffer(df))


def test_parse_telemetry_csv_rejects_non_numeric_values():
    df = generate_mock_telemetry(num_records=3)
    df['comms_link'] = df['comms_link'].astype(object)
    df.loc[2, 'comms_link'] = 'not-a-number'

    with pytest.raises(ValueError, match='comms_link'):
        parse_telemetry_csv(_csv_buffer(df))
