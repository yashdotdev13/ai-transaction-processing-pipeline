import pandas as pd


class AnomalyDetector:

    DOMESTIC_ONLY_MERCHANTS = {
        "SWIGGY",
        "OLA",
        "IRCTC",
    }

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        # Default columns
        df["is_anomaly"] = False
        df["anomaly_reason"] = ""

        # Calculate median transaction amount for each account
        account_medians = (
            df.groupby("account_id")["amount"]
            .median()
            .to_dict()
        )

        for index, row in df.iterrows():

            reasons = []

            account_id = str(row["account_id"])
            amount = float(row["amount"])

            median_amount = account_medians.get(account_id, 0)

            if (
                median_amount > 0
                and amount > (median_amount * 3)
            ):
                reasons.append(
                    "Amount exceeds 3x account median"
                )

            merchant = str(row["merchant"]).strip().upper()
            currency = str(row["currency"]).strip().upper()

            if (
                currency == "USD"
                and merchant in self.DOMESTIC_ONLY_MERCHANTS
            ):
                reasons.append(
                    "USD used with domestic merchant"
                )

            # Save anomaly information
            if reasons:
                df.at[index, "is_anomaly"] = True
                df.at[index, "anomaly_reason"] = "; ".join(reasons)

        return df