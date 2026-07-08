import sys
import os

# Adjust path to find core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.core.ingestion import generate_mock_telemetry, score_anomalies

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
    assert scored.loc[30, 'cpu_anomaly'] == True
    assert scored.loc[30, 'temp_anomaly'] == True
    assert scored.loc[30, 'risk_score'] > 0
