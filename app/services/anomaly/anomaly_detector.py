import pandas as pd


class AnomalyDetector:

    HIGH_AMOUNT_THRESHOLD = 10000

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        # Default values
        df["is_anomaly"] = False
        df["anomaly_reason"] = ""

        for index, row in df.iterrows():

            reasons = []


            if row["amount"] > self.HIGH_AMOUNT_THRESHOLD:
                reasons.append("High Amount")


            if str(row["status"]).upper() == "FAILED":
                reasons.append("Failed Transaction")


            notes = str(row["notes"]).upper()

            if "SUSPICIOUS" in notes:
                reasons.append("Suspicious Notes")


            if str(row["currency"]).upper() != "INR":
                reasons.append("Foreign Currency")


            if row["date"].weekday() >= 5:
                reasons.append("Weekend Transaction")

            if "REFUND" in notes:
                reasons.append("Refund Transaction")

            if reasons:
                df.at[index, "is_anomaly"] = True
                df.at[index, "anomaly_reason"] = ", ".join(reasons)

        return df