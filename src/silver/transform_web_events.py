import pandas as pd
from pathlib import Path

BRONZE_PATH = "/opt/airflow/data/bronze/web_events/"
SILVER_PATH = "/opt/airflow/data/silver/web_events/web_events.parquet"

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
    # Drop duplicates per event
    df = (
        df.sort_values("ingestion_timestamp")
        .drop_duplicates(subset=["event_id"], keep="last")
    )

    # Cast columns safely
    df["product_id"] = df["product_id"].astype("Int64")       # nullable int
    df["customer_id"] = df["customer_id"].astype("Int64")     # nullable int
    df["event_id"] = df["event_id"].astype("string")          # UUID string
    df["session_id"] = df["session_id"].astype("string")      # UUID string

    df.to_parquet(SILVER_PATH, index=False)

    print("Silver web events written successfully")


if __name__ == "__main__":
    main()
