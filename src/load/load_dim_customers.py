import pandas as pd
from sqlalchemy import create_engine

# Connection
engine = create_engine(
    "postgresql+psycopg2://admin:admin@localhost:5432/dwh"
)

# Load parquet
df = pd.read_parquet("data/gold/dimensions/dim_customers.parquet")

# Load to PostgreSQL
df.to_sql(
    "dim_customers",
    engine,
    if_exists="replace",
    index=False
)

print("dim_customers loaded successfully")