import pandas as pd
from pathlib import Path

BRONZE_PATH = "data/bronze/products/"
SILVER_PATH = "data/silver/products/products.parquet"

Path(SILVER_PATH).parent.mkdir(parents=True, exist_ok=True)

# Read entire Bronze dataset (partition-aware)
df = pd.read_parquet(
    BRONZE_PATH,
    engine="pyarrow"
)

# Normalize metadata columns
df["ingestion_date"] = df["ingestion_date"].astype("string")
df["ingestion_timestamp"] = pd.to_datetime(df["ingestion_timestamp"])

# Drop bad records
df = df.dropna(subset=["product_id"])

# Deduplicate (latest record per product)
df = (
    df.sort_values("ingestion_timestamp")
      .drop_duplicates(subset=["product_id"], keep="last")
)

# Enforce schema
df["product_id"] = df["product_id"].astype(int)

# Write Silver table
df.to_parquet(SILVER_PATH, index=False)

print("Silver products written successfully")
