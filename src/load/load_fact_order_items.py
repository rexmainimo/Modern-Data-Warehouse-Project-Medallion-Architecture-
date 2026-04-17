import pandas as pd
from sqlalchemy import create_engine

# Connection
engine = create_engine(
    "postgresql+psycopg2://admin:admin@localhost:5432/dwh"
)

df = pd.read_parquet("data/gold/facts/fact_order_items.parquet")

df.to_sql("fact_order_items", engine, if_exists="replace", index=False)
print("fact_order_items loaded successfully")