# Data Contract: Telemetry Ingestion

**Artifact:** Mission Autonomy Field Support Console  
**Version:** 1.0  
**Owner:** FDE-Team-01

## Purpose

Define the input schema, validation rules, and scored output fields for local telemetry ingestion. All ingestion and scoring logic lives in `src/core/ingestion.py`; the Streamlit app consumes scored frames only.

## Input: `telemetry.csv`

### Required columns

| Column | Type | Unit / range | Description |
|---|---|---|---|
| `timestamp` | datetime (ISO 8601) | UTC preferred | Sample time |
| `battery_level` | float | 0–100 % | Remaining battery |
| `cpu_utilization` | float | 0–100 % | Compute load |
| `sensor_drift` | float | ≥ 0 | IMU/sensor drift magnitude |
| `comms_link` | float | 0–100 % | Link quality score |
| `temperature` | float | °C | Core or enclosure temperature |

### Validation rules

- All six columns must be present; missing columns raise `ValueError` with column names listed.
- `timestamp` is parsed with `parse_dates=['timestamp']`.
- Extra columns are ignored by the starter contract (future: warn in governance panel).

### Reference implementation

- `validate_telemetry_schema(df)` — column presence check
- `parse_telemetry_csv(source)` — path or file-like object
- `load_telemetry_csv(path)` — filesystem path wrapper

### Fixture

- `fixtures/sample_telemetry.csv` — 50 records with injected anomalies at indices 10 (sensor drift) and 30 (CPU + temperature).

## Scoring thresholds

| Signal | Threshold | Anomaly flag | Risk weight |
|---|---|---|---|
| CPU utilization | > 85.0 % | `cpu_anomaly` | 30 |
| Temperature | > 80.0 °C | `temp_warning` | 20 |
| Temperature | > 85.0 °C | `temp_critical` (+10 risk) | 10 |
| Sensor drift | > 0.3 | `sensor_anomaly` | 20 |
| Comms link | < 80.0 % | `comms_anomaly` | 20 |

`temp_anomaly` mirrors `temp_warning` for backward compatibility in the UI.

## Output: scored telemetry frame

All input columns are preserved. Added columns:

| Column | Type | Description |
|---|---|---|
| `cpu_anomaly` | bool | CPU above threshold |
| `temp_warning` | bool | Temperature in warning band |
| `temp_critical` | bool | Temperature in critical band |
| `temp_anomaly` | bool | Alias for `temp_warning` |
| `sensor_anomaly` | bool | Drift above threshold |
| `comms_anomaly` | bool | Link below threshold |
| `risk_score` | int | 0–100 composite index |

## Operator action log (separate contract)

**Path:** `artifacts/operator_action_log.csv` (runtime-generated, gitignored)

| Column | Type | Description |
|---|---|---|
| `timestamp` | ISO 8601 UTC | Action time |
| `operator` | string | Operator ID |
| `asset_id` | string | Asset under triage |
| `disposition` | enum | Observed, Mitigated, Escalated, Deferred |
| `action` | string | Free-text diagnostic note |

## JSON schemas

Machine-readable contracts in `src/schemas/`:

| File | Validates |
|---|---|
| `input_schema.json` | Raw telemetry row |
| `output_schema.json` | Scored telemetry row |
| `rca_packet_schema.json` | Engineering RCA export from `src/core/exports.py` |

Golden regression summary: `tests/golden_outputs/fixture_scoring_summary.json`

## RCA export

- **Builder:** `build_rca_packet()` in `src/core/exports.py`
- **Output dir:** `artifacts/exports/` (gitignored contents; `.gitkeep` only)
- **Formats:** JSON + Markdown per export

## DuckDB store (Mission Console)

- **Module:** `src/core/duckdb_store.py`
- **Database:** `artifacts/mission_console.duckdb` (local file, gitignored)
- **Tables:** `ingest_sessions`, `telemetry_scored`
- **Flow:** Python scores via `score_anomalies()` → persisted to DuckDB → UI/SQL reads alerts

## Future extensions

- Polars adapters for files > 100 MB
- Parquet ingestion
- Full golden CSV hash comparison for entire scored frame

## Governance disclosure (UI)

Every scored session must surface:

- Data source label (mock, fixture path, or upload filename)
- Record count
- Last refresh (`max(timestamp)`)
- Test status reference (`pytest: ingestion suite`)