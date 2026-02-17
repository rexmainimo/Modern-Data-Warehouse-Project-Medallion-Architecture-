import pandas as pd
from pathlib import Path

BRONZE_PATH = "data/bronze/payments/"
SILVER_PATH = "data/silver/payments/payments.parquet"

Path(SILVER_PATH).parent.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(
    BRONZE_PATH,
    engine="pyarrow"
)

# Partition column inferred by Arrow
df["ingestion_date"] = df["ingestion_date"].astype("string")
df["ingestion_timestamp"] = pd.to_datetime(df["ingestion_timestamp"])

# Business rules
df = df.dropna(subset=["payment_id", "order_id"])

df = (
    df.sort_values("ingestion_timestamp")
      .drop_duplicates(subset=["payment_id"], keep="last")
)

df["payment_id"] = df["payment_id"].astype(int)
df["order_id"] = df["order_id"].astype(int)

df.to_parquet(SILVER_PATH, index=False)

print("Silver payments written successfully")