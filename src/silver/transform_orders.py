import pandas as pd
from pathlib import Path

BRONZE_PATH = "/opt/airflow/data/bronze/orders/"
SILVER_PATH = "/opt/airflow/data/silver/orders/orders.parquet"

def main():
    Path(SILVER_PATH).parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(
        BRONZE_PATH,
        engine="pyarrow"
    )

    # Partition column inferred by Arrow
    df["ingestion_date"] = df["ingestion_date"].astype("string")
    df["ingestion_timestamp"] = pd.to_datetime(df["ingestion_timestamp"])

    # Business rules
    df = df.dropna(subset=["order_id", "customer_id"])

    df = (
        df.sort_values("ingestion_timestamp")
        .drop_duplicates(subset=["order_id"], keep="last")
    )

    df["order_id"] = df["order_id"].astype(int)
    df["customer_id"] = df["customer_id"].astype(int)

    df.to_parquet(SILVER_PATH, index=False)

    print("Silver orders written successfully")

if __name__ == "__main__":
    main()
