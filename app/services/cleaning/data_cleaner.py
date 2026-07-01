import pandas as pd


class DataCleaner:

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        string_columns = df.select_dtypes(include=["object"]).columns

        for column in string_columns:
            df[column] = (
                df[column]
                .astype(str)
                .str.strip()
            )

        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        )

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce",
            dayfirst=True
        )

        df["currency"] = (
            df["currency"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        df["status"] = (
            df["status"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        df["category"] = (
            df["category"]
            .fillna("")
            .astype(str)
            .replace("nan", "")
            .str.strip()
        )

        df.loc[
            df["category"] == "",
            "category"
        ] = "Uncategorised"

        df["notes"] = (
            df["notes"]
            .fillna("")
            .astype(str)
            .replace("nan", "")
            .str.strip()
        )

        df = df.dropna(subset=["amount"])

        df = df.dropna(subset=["date"])

        df = df.drop_duplicates()

        df = df.reset_index(drop=True)

        return df