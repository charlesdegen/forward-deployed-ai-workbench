import json
import os

from src.core.ingestion import load_telemetry_csv, score_anomalies


ANOMALY_FLAGS = (
    "cpu_anomaly",
    "temp_warning",
    "temp_critical",
    "sensor_anomaly",
    "comms_anomaly",
)


def _fixture_summary():
    fixture_path = os.path.join(os.path.dirname(__file__), "..", "fixtures", "sample_telemetry.csv")
    scored = score_anomalies(load_telemetry_csv(fixture_path))
    return {
        "record_count": len(scored),
        "alert_count": int((scored["risk_score"] > 0).sum()),
        "max_risk_score": int(scored["risk_score"].max()),
        "alert_indices": sorted(scored.index[scored["risk_score"] > 0].tolist()),
        # Every flag is pinned so a threshold regression on any one of them fails here.
        "flag_counts": {flag: int(scored[flag].sum()) for flag in ANOMALY_FLAGS},
        "index_30": {
            "cpu_anomaly": bool(scored.loc[30, "cpu_anomaly"]),
            "temp_critical": bool(scored.loc[30, "temp_critical"]),
            "risk_score": int(scored.loc[30, "risk_score"]),
        },
        # Comms-only degradation: isolates the comms branch and its risk weight.
        "index_41": {
            "comms_anomaly": bool(scored.loc[41, "comms_anomaly"]),
            "cpu_anomaly": bool(scored.loc[41, "cpu_anomaly"]),
            "risk_score": int(scored.loc[41, "risk_score"]),
        },
        # Full cascade: pins the 0-100 upper bound of the composite index.
        "index_45": {flag: bool(scored.loc[45, flag]) for flag in ANOMALY_FLAGS}
        | {"risk_score": int(scored.loc[45, "risk_score"])},
        # Warning band without critical: pins the 80-85 temperature split.
        "index_47": {
            "temp_warning": bool(scored.loc[47, "temp_warning"]),
            "temp_critical": bool(scored.loc[47, "temp_critical"]),
            "risk_score": int(scored.loc[47, "risk_score"]),
        },
        "index_10_sensor_anomaly": bool(scored.loc[10, "sensor_anomaly"]),
    }


def test_fixture_scoring_matches_golden_summary():
    golden_path = os.path.join(
        os.path.dirname(__file__), "golden_outputs", "fixture_scoring_summary.json"
    )
    with open(golden_path, encoding="utf-8") as handle:
        expected = json.load(handle)

    actual = _fixture_summary()
    assert actual == expected