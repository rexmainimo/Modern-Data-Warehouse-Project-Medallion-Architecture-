import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

SOURCE_FILE = "data/raw/web_events.json"
BRONZE_PATH = "data/bronze/web_events/"

df = pd.read_json(SOURCE_FILE, lines=True)

ingestion_time = datetime.now(timezone.utc)
df["ingestion_timestamp"] = ingestion_time
df["ingestion_date"] = ingestion_time.date().isoformat()
df["source_file"] = SOURCE_FILE

partition_path = (
    Path(BRONZE_PATH)
    / f"ingestion_date={df['ingestion_date'].iloc[0]}"
)
partition_path.mkdir(parents=True, exist_ok=True)

output_file = partition_path / f"web_events_{ingestion_time.strftime('%H%M%S')}.parquet"

df.to_parquet(
    output_file,
    engine="pyarrow",
    index=False
)

print(f"Ingested {len(df)} events into {output_file}")
