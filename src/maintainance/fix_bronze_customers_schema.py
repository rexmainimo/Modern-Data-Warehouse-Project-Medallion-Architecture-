

# BRONZE_FILE = (
#     "data/bronze/customers/"
#     "ingestion_date=2026-02-04/"
#     "customers_171918.parquet"
# )

import pandas as pd
import glob

BRONZE_PATH = "data/bronze/customers/ingestion_date=2026-02-04/customers_171918"

files = glob.glob(
    BRONZE_PATH + "**/*.parquet",
    recursive=True
)

print(f"Fixing {len(files)} files")

for f in files:
    df = pd.read_parquet(f)

    # ❌ remove partition columns
    df = df.drop(columns=["ingestion_date"], errors="ignore")

    # ✅ normalize timestamps
    if "ingestion_timestamp" in df.columns:
        df["ingestion_timestamp"] = pd.to_datetime(df["ingestion_timestamp"])

    df.to_parquet(f, index=False)

print("Bronze schema fixed successfully")
