import pandas as pd
from sqlalchemy import create_engine

# Connection
engine = create_engine(
    "postgresql+psycopg2://admin:admin@localhost:5432/dwh"
)

df = pd.read_parquet("data/gold/facts/fact_web_events.parquet")

df.to_sql("fact_web_events", engine, if_exists="replace", index=False) 
print("fact_web_events loaded successfully")