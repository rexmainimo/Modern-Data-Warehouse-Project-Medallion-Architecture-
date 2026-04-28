import pandas as pd
from pathlib import Path

BRONZE_PATH = "/opt/airflow/data/bronze/customers/"
SILVER_PATH = "/opt/airflow/data/silver/customers/customers.parquet"

def main():
    Path(SILVER_PATH).parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(
        BRONZE_PATH,
        engine="pyarrow"
    )

    # Arrow injects ingestion_date from partition path
    df["ingestion_date"] = df["ingestion_date"].astype("string")
    df["ingestion_timestamp"] = pd.to_datetime(df["ingestion_timestamp"])

    # Business logic
    df = df.dropna(subset=["customer_id"])

    df = (
        df.sort_values("ingestion_timestamp")
          .drop_duplicates(subset=["customer_id"], keep="last")
    )

    df["customer_id"] = df["customer_id"].astype(int)

    df.to_parquet(SILVER_PATH, index=False)

    print("Silver customers written successfully")


if __name__ == "__main__":
    main()

