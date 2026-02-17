import pandas as pd
from datetime import datetime, timezone
from pathlib import Path
import os 

SOURCE_FILE = "data/raw/customers.csv"
BRONZE_PATH = "data/bronze/customers/"

print("Current working directory:", os.getcwd())
# Read raw CSV
df = pd.read_csv(SOURCE_FILE)

# Add ingestion metadata
ingestion_time = datetime.now(timezone.utc)
df["ingestion_timestamp"] = ingestion_time
df["ingestion_date"] = ingestion_time.date().isoformat()
df["source_file"] = SOURCE_FILE

# Create partition path
partition_path = (
    Path(BRONZE_PATH)
    / f"ingestion_date={df['ingestion_date'].iloc[0]}"
)
partition_path.mkdir(parents=True, exist_ok=True)

# Write Parquet (append-style)
output_file = partition_path / f"customers_{ingestion_time.strftime('%H%M%S')}.parquet"

df.to_parquet(
    output_file,
    engine="pyarrow",
    index=False
)

print(f"Ingested {len(df)} rows into {output_file}")
