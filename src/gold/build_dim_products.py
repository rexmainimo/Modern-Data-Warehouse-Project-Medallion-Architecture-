import pandas as pd
from pathlib import Path

SILVER_PATH = 'Data/silver/products/products.parquet'
GOLD_PATH = 'Data/gold/dimensions/dim_products.parquet'

Path(GOLD_PATH).parent.mkdir(parents=True, exist_ok=True)

df = pd.read_parquet(SILVER_PATH)

df = df.sort_values('product_id').reset_index(drop=True)
df['product_key'] = df.index + 1
df['current_price'] = df['price']
df['is_available'] = True
dim_products = df[
    [
        "product_key",
        "product_id",
        "product_name",
        "category",
        "current_price",
        #"description",
        "is_available"
    ]
]
dim_products.to_parquet(GOLD_PATH, index=False)

print("dim_products built successfully")