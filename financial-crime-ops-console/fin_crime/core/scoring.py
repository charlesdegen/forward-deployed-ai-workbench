"""Deterministic AML-style risk scoring for synthetic transaction alerts.

Thresholds are intentionally transparent and offline — no model inference.
"""

from __future__ import annotations

import pandas as pd

# Amount bands (USD)
AMOUNT_ELEVATED = 10_000.0
AMOUNT_HIGH = 50_000.0
AMOUNT_CRITICAL = 100_000.0

# Structuring: multiple transactions just under reporting threshold
STRUCTURING_CEILING = 9_900.0
STRUCTURING_FLOOR = 8_000.0

HIGH_RISK_COUNTRIES = frozenset({"XX", "YY", "ZZ"})  # synthetic jurisdiction codes

# Minimum risk a case must carry to reach the operator queue. Surfaces import this
# rather than restating the number, so the queue cutoff has one definition.
CASE_QUEUE_MIN_SCORE = 25


def score_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Add risk_score (0–100), risk_band, and flag columns."""
    out = df.copy()
    scores = []
    bands = []
    flags_list = []

    for _, row in out.iterrows():
        score = 0
        flags: list[str] = []
        amount = float(row["amount_usd"])

        if amount >= AMOUNT_CRITICAL:
            score += 40
            flags.append("amount_critical")
        elif amount >= AMOUNT_HIGH:
            score += 25
            flags.append("amount_high")
        elif amount >= AMOUNT_ELEVATED:
            score += 12
            flags.append("amount_elevated")

        if STRUCTURING_FLOOR <= amount <= STRUCTURING_CEILING:
            score += 18
            flags.append("near_threshold_structuring")

        if bool(row["is_cross_border"]):
            score += 10
            flags.append("cross_border")

        origin = str(row["country_origin"]).upper()
        dest = str(row["country_dest"]).upper()
        if origin in HIGH_RISK_COUNTRIES or dest in HIGH_RISK_COUNTRIES:
            score += 20
            flags.append("high_risk_jurisdiction")

        prior = int(row["prior_sar_count"])
        if prior >= 2:
            score += 15
            flags.append("repeat_sar_subject")
        elif prior == 1:
            score += 8
            flags.append("prior_sar")

        channel = str(row["channel"]).lower()
        if channel in {"crypto_onramp", "wire", "cash_deposit"}:
            score += 8
            flags.append(f"channel_{channel}")

        score = min(100, score)
        if score >= 70:
            band = "CRITICAL"
        elif score >= 45:
            band = "HIGH"
        elif score >= 25:
            band = "MEDIUM"
        else:
            band = "LOW"

        scores.append(score)
        bands.append(band)
        flags_list.append("|".join(flags) if flags else "none")

    out["risk_score"] = scores
    out["risk_band"] = bands
    out["risk_flags"] = flags_list
    out["case_status"] = "OPEN"
    return out


def case_queue(scored: pd.DataFrame, min_score: int = CASE_QUEUE_MIN_SCORE) -> pd.DataFrame:
    """Return open cases ordered by risk, excluding low-noise rows."""
    queue = scored[scored["risk_score"] >= min_score].copy()
    return queue.sort_values(["risk_score", "timestamp"], ascending=[False, True]).reset_index(drop=True)
