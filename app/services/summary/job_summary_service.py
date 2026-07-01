from collections import Counter

import pandas as pd


class JobSummaryService:

    def generate(self, df: pd.DataFrame) -> dict:

        total_spend_inr = (
            df[df["currency"].str.upper() == "INR"]["amount"]
            .sum()
        )

        total_spend_usd = (
            df[df["currency"].str.upper() == "USD"]["amount"]
            .sum()
        )

        top_merchants = (
            Counter(df["merchant"])
            .most_common(5)
        )

        category_breakdown = (
            df["llm_category"]
            .fillna("Other")
            .value_counts()
            .to_dict()
        )

        anomaly_count = int(
            df["is_anomaly"].sum()
        )

        if anomaly_count >= 20:
            risk = "HIGH"
        elif anomaly_count >= 10:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        return {
            "total_spend_inr": float(total_spend_inr),
            "total_spend_usd": float(total_spend_usd),
            "top_merchants": dict(top_merchants),
            "category_breakdown": category_breakdown,
            "anomaly_count": anomaly_count,
            "risk_level": risk,
        }