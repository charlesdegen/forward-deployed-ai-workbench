import json
from functools import lru_cache
from pathlib import Path

import pandas as pd
import numpy as np

REQUIRED_TELEMETRY_COLUMNS = {
    'timestamp',
    'battery_level',
    'cpu_utilization',
    'sensor_drift',
    'comms_link',
    'temperature',
}

CPU_ANOMALY_THRESHOLD = 85.0
TEMP_WARNING_THRESHOLD = 80.0
TEMP_CRITICAL_THRESHOLD = 85.0
SENSOR_DRIFT_THRESHOLD = 0.3
COMMS_LINK_THRESHOLD = 80.0

# A row is an alert when any anomaly flag contributes risk.
ALERT_RISK_THRESHOLD = 0

INPUT_SCHEMA_PATH = Path(__file__).resolve().parents[1] / 'schemas' / 'input_schema.json'


def generate_mock_telemetry(num_records: int = 50) -> pd.DataFrame:
    """Generates synthetic telemetry data for testing.
    
    Args:
        num_records: Number of telemetry records to generate.
    """
    np.random.seed(42)
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=num_records, freq='s')
    
    # Base normal signals
    battery_level = np.clip(100.0 - (np.arange(num_records) * 0.1) + np.random.normal(0, 0.1, num_records), 0.0, 100.0)
    cpu_utilization = np.clip(30.0 + np.random.normal(0, 5.0, num_records), 0.0, 100.0)
    # Drift is a magnitude: the data contract publishes sensor_drift >= 0.
    sensor_drift = np.clip(np.random.normal(0.02, 0.005, num_records), 0.0, None)
    comms_link = np.clip(95.0 + np.random.normal(0, 1.0, num_records), 0.0, 100.0)
    temperature = 45.0 + np.arange(num_records) * 0.05 + np.random.normal(0, 0.2, num_records)

    # Introduce synthetic anomalies
    # Anomaly 1: Sudden CPU spike and temperature surge at step 30
    if num_records > 30:
        cpu_utilization[30:35] = 98.5
        temperature[30:35] = 88.2
    # Anomaly 2: Sensor drift spike at step 10
    if num_records > 10:
        sensor_drift[10:13] = 0.45
    # Anomaly 3: Comms link degradation at step 20
    if num_records > 20:
        comms_link[20:23] = 62.0

    df = pd.DataFrame({
        'timestamp': timestamps,
        'battery_level': battery_level,
        'cpu_utilization': cpu_utilization,
        'sensor_drift': sensor_drift,
        'comms_link': comms_link,
        'temperature': temperature
    })
    
    return df


def validate_telemetry_schema(df: pd.DataFrame) -> None:
    """Raises ValueError when required telemetry columns are missing."""
    missing = REQUIRED_TELEMETRY_COLUMNS.difference(df.columns)
    if missing:
        missing_list = ', '.join(sorted(missing))
        raise ValueError(f"Missing required telemetry columns: {missing_list}")


@lru_cache(maxsize=1)
def _schema_numeric_bounds() -> tuple[tuple[str, float | None, float | None], ...]:
    """Reads the published numeric bounds from `src/schemas/input_schema.json`.

    The schema is the source of truth for the ranges advertised in
    `specs/data_contract.md`; ingestion binds to it rather than restating them.
    """
    schema = json.loads(INPUT_SCHEMA_PATH.read_text(encoding='utf-8'))
    bounds = []
    for column, prop in schema.get('properties', {}).items():
        if prop.get('type') != 'number':
            continue
        bounds.append((column, prop.get('minimum'), prop.get('maximum')))
    return tuple(bounds)


def validate_telemetry_ranges(df: pd.DataFrame) -> None:
    """Raises ValueError when numeric columns violate the published input schema bounds."""
    violations: list[str] = []

    for column, minimum, maximum in _schema_numeric_bounds():
        if column not in df.columns:
            continue

        values = pd.to_numeric(df[column], errors='coerce')
        non_numeric = int(values.isna().sum()) - int(df[column].isna().sum())
        if non_numeric > 0:
            violations.append(f"{column}: {non_numeric} non-numeric value(s)")
            continue

        if minimum is not None:
            below = int((values < minimum).sum())
            if below:
                violations.append(f"{column}: {below} value(s) below minimum {minimum}")
        if maximum is not None:
            above = int((values > maximum).sum())
            if above:
                violations.append(f"{column}: {above} value(s) above maximum {maximum}")

    if violations:
        raise ValueError(f"Telemetry range violations: {'; '.join(sorted(violations))}")


def parse_telemetry_csv(source) -> pd.DataFrame:
    """Loads telemetry CSV from a file path or file-like object and validates schema and ranges."""
    df = pd.read_csv(source, parse_dates=['timestamp'])
    validate_telemetry_schema(df)
    validate_telemetry_ranges(df)
    return df


def load_telemetry_csv(path: str) -> pd.DataFrame:
    """Loads local telemetry CSV data and validates the expected schema."""
    return parse_telemetry_csv(path)


def score_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Applies thresholds to highlight anomalies in the telemetry log.
    
    Args:
        df: Input DataFrame containing telemetry columns.
    """
    validate_telemetry_schema(df)

    scored = df.copy()
    scored['cpu_anomaly'] = scored['cpu_utilization'] > CPU_ANOMALY_THRESHOLD
    scored['temp_warning'] = scored['temperature'] > TEMP_WARNING_THRESHOLD
    scored['temp_critical'] = scored['temperature'] > TEMP_CRITICAL_THRESHOLD
    scored['temp_anomaly'] = scored['temp_warning']
    scored['sensor_anomaly'] = scored['sensor_drift'] > SENSOR_DRIFT_THRESHOLD
    scored['comms_anomaly'] = scored['comms_link'] < COMMS_LINK_THRESHOLD
    
    # Overall risk score (0-100)
    scored['risk_score'] = (
        (scored['cpu_anomaly'].astype(int) * 30) +
        (scored['temp_warning'].astype(int) * 20) +
        (scored['temp_critical'].astype(int) * 10) +
        (scored['sensor_anomaly'].astype(int) * 20) +
        (scored['comms_anomaly'].astype(int) * 20)
    )

    return scored


def alert_mask(scored_df: pd.DataFrame) -> pd.Series:
    """Boolean mask of rows that qualify as operator alerts."""
    return scored_df['risk_score'] > ALERT_RISK_THRESHOLD


def count_alerts(scored_df: pd.DataFrame) -> int:
    """Number of scored rows carrying any risk."""
    return int(alert_mask(scored_df).sum())


def derive_system_state(alert_count: int) -> str:
    """Maps an alert count to the operator-facing system state."""
    return 'DEGRADED' if alert_count > 0 else 'NOMINAL'


def summarize_alert_state(scored_df: pd.DataFrame) -> dict:
    """Single source of truth for alert count and system state across every surface."""
    alert_count = count_alerts(scored_df)
    return {
        'alert_count': alert_count,
        'system_state': derive_system_state(alert_count),
    }
