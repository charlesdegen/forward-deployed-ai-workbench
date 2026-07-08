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
    sensor_drift = np.random.normal(0.02, 0.005, num_records)
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


def parse_telemetry_csv(source) -> pd.DataFrame:
    """Loads telemetry CSV from a file path or file-like object and validates schema."""
    df = pd.read_csv(source, parse_dates=['timestamp'])
    validate_telemetry_schema(df)
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
