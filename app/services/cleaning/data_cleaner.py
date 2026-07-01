import pandas as pd


class DataCleaner:

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:

        # Create a copy
        df = df.copy()

        # Remove leading/trailing spaces
        string_columns = df.select_dtypes(include=["object"]).columns

        for column in string_columns:
            df[column] = df[column].astype(str).str.strip()

        # Replace NaN in notes
        if "notes" in df.columns:
            df["notes"] = df["notes"].replace("nan", "")

        # Convert amount to numeric
        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        )

        # Remove rows where amount is invalid
        df = df.dropna(subset=["amount"])

        # Convert dates
        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
            dayfirst=True
        )

        # Remove invalid dates
        df = df.dropna(subset=["date"])

        # Remove duplicate transaction IDs
        df = df.drop_duplicates(
            subset=["txn_id"]
        )

        return df