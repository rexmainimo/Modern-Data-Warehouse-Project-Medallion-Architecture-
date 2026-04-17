import pandas as pd
from sqlalchemy import create_engine

# Connection
engine = create_engine(
    "postgresql+psycopg2://admin:admin@localhost:5432/dwh"
)

df = pd.read_parquet("data/gold/dimensions/dim_date.parquet")

df.to_sql("dim_date", engine, if_exists="replace", index=False)

print("dim_date loaded successfully")