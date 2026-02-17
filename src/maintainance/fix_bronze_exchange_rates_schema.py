import pandas as pd
import glob
from pathlib import Path

BRONZE_PATH = "data/bronze/exchangeRates/"
FIXED_PATH = "data/bronze_fixed/exchange_rates/exchange_rates_fixed.parquet"

Path(FIXED_PATH).parent.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 1️⃣ Find all parquet files recursively
# --------------------------------------------------

files = glob.glob(f"{BRONZE_PATH}/**/*.parquet", recursive=True)

if not files:
    raise ValueError("No parquet files found in Bronze exchangeRates")

dfs = []

# --------------------------------------------------
# 2️⃣ Read each file individually
# --------------------------------------------------

for f in files:
    df = pd.read_parquet(f)

    # Drop partition & metadata columns early
    df = df.drop(columns=["ingestion_date"], errors="ignore")

    dfs.append(df)

print(f"Found {len(dfs)} parquet files")

# --------------------------------------------------
# 3️⃣ Concatenate manually (safe)
# --------------------------------------------------

df = pd.concat(dfs, ignore_index=True)

# --------------------------------------------------
# 4️⃣ Standardize schema
# --------------------------------------------------

df.columns = df.columns.str.lower().str.strip()

df = df.rename(columns={
    "rate_date": "date",
    "base_currency": "source_currency",
    "exchange_rate": "rate"
})

# --------------------------------------------------
# 5️⃣ Fix data types
# --------------------------------------------------

df["date"] = pd.to_datetime(df["date"])
df["source_currency"] = df["source_currency"].astype("string")
df["target_currency"] = df["target_currency"].astype("string")
df["rate"] = df["rate"].astype(float)

if "ingestion_timestamp" in df.columns:
    df["ingestion_timestamp"] = pd.to_datetime(df["ingestion_timestamp"])

# --------------------------------------------------
# 6️⃣ Save fixed bronze
# --------------------------------------------------

df.to_parquet(FIXED_PATH, index=False)

print("Bronze exchange_rates schema fixed successfully")
