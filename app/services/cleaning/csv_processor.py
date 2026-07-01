import pandas as pd


class CSVProcessor:
    REQUIRED_COLUMNS = [
        "txn_id",
        "date",
        "merchant",
        "amount",
        "currency",
        "status",
        "category",
        "account_id",
        "notes",
    ]

    def read_csv(self, file_path: str):
        return pd.read_csv(file_path)

    def validate_columns(self, df):
        csv_columns = [col.strip().lower() for col in df.columns]

        missing = [
            col
            for col in self.REQUIRED_COLUMNS
            if col.lower() not in csv_columns
        ]

        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    def process(self, file_path: str):
        df = self.read_csv(file_path)

        self.validate_columns(df)

        return df