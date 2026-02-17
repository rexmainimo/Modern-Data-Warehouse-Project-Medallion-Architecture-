import pandas as pd
from pathlib import Path

BRONZE_FIXED_PATH = "data/bronze_fixed/exchange_rates/exchange_rates_fixed.parquet"
SILVER_PATH = "data/silver/exchange_rates/exchange_rates.parquet"

Path(SILVER_PATH).parent.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(BRONZE_FIXED_PATH)

# -------------------------------------------
# Remove duplicates
# -------------------------------------------

df = df.drop_duplicates(
    subset=["source_currency", "target_currency", "date"],
    keep="last"
)

# -------------------------------------------
# Keep only business columns
# -------------------------------------------

df = df[[
    "source_currency",
    "target_currency",
    "date",
    "rate"
]]

df.to_parquet(SILVER_PATH, index=False)

print("Silver exchange_rates written successfully")
