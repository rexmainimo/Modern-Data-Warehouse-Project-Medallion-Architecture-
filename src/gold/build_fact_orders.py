import pandas as pd
from pathlib import Path

# Paths
ORDERS_PATH = "data/silver/orders/orders.parquet"
CUSTOMERS_PATH = "data/gold/dimensions/dim_customers.parquet"
PRODUCTS_PATH = "data/gold/dimensions/dim_products.parquet"
DATE_PATH = "data/gold/dimensions/dim_date.parquet"
FX_PATH = "data/silver/exchange_rates/exchange_rates.parquet"

GOLD_PATH = "data/gold/facts/fact_orders.parquet"
Path(GOLD_PATH).parent.mkdir(parents=True, exist_ok=True)

# Load data
orders = pd.read_parquet(ORDERS_PATH)
customers = pd.read_parquet(CUSTOMERS_PATH)
products = pd.read_parquet(PRODUCTS_PATH)
dates = pd.read_parquet(DATE_PATH)
fx = pd.read_parquet(FX_PATH)


orders = orders.merge(
    customers[["customer_id", "customer_key"]],
    on="customer_id",
    how="left"
)

orders = orders.merge(
    products[["product_id", "product_key"]],
    on="product_id",
    how="left"
)

orders["order_date"] = pd.to_datetime(orders["order_timestamp"]).dt.date

orders = orders.merge(
    dates[["date", "date_key"]],
    left_on="order_date",
    right_on="date",
    how="left"
)

orders = orders.rename(columns={"date_key": "order_date_key"})
orders = orders.drop(columns=["date"])

fx["rate_date"] = pd.to_datetime(fx["rate_date"]).dt.date

orders = orders.merge(
    fx,
    left_on=["order_date", "currency"],
    right_on=["rate_date", "target_currency"],
    how="left"
)

orders["order_amount_eur"] = (
    orders["order_amount_local"] / orders["exchange_rate"]
)

fact_orders = orders[
    [
        "order_id",
        "customer_key",
        "product_key",
        "order_date_key",
        "currency",
        "order_amount_local",
        "order_amount_eur",
        "quantity"
    ]
]

# Drop orders missing mandatory keys
fact_orders = fact_orders.dropna(
    subset=["customer_key", "product_key", "order_date_key"]
)

fact_orders.to_parquet(GOLD_PATH, index=False)
print("fact_orders built successfully")

