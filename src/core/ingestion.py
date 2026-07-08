import pandas as pd
import numpy as np

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

def score_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """Applies thresholds to highlight anomalies in the telemetry log.
    
    Args:
        df: Input DataFrame containing telemetry columns.
    """
    scored = df.copy()
    scored['cpu_anomaly'] = scored['cpu_utilization'] > 85.0
    scored['temp_anomaly'] = scored['temperature'] > 80.0
    scored['sensor_anomaly'] = scored['sensor_drift'] > 0.3
    scored['comms_anomaly'] = scored['comms_link'] < 80.0
    
    # Overall risk score (0-100)
    scored['risk_score'] = (
        (scored['cpu_anomaly'].astype(int) * 30) +
        (scored['temp_anomaly'].astype(int) * 30) +
        (scored['sensor_anomaly'].astype(int) * 20) +
        (scored['comms_anomaly'].astype(int) * 20)
    )
    
    return scored
