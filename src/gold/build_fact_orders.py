import pandas as pd
from pathlib import Path

ORDERS_PATH = "data/silver/orders/orders.parquet"
CUSTOMERS_PATH = "data/gold/dimensions/dim_customers.parquet"
DATE_PATH = "data/gold/dimensions/dim_date.parquet"
ORDER_ITEMS_PATH = "data/gold/facts/fact_order_items.parquet"

GOLD_PATH = "data/gold/facts/fact_orders.parquet"
Path(GOLD_PATH).parent.mkdir(parents=True, exist_ok=True)

# -----------------------------------------
# 1️⃣ Load Data
# -----------------------------------------

orders = pd.read_parquet(ORDERS_PATH)
customers = pd.read_parquet(CUSTOMERS_PATH)
dates = pd.read_parquet(DATE_PATH)
order_items = pd.read_parquet(ORDER_ITEMS_PATH)

# -----------------------------------------
# 2️⃣ Date Handling
# -----------------------------------------

orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["order_date"] = orders["order_date"].dt.normalize()

dates["date"] = pd.to_datetime(dates["date"])

orders = orders.merge(
    dates[["date", "date_key"]],
    left_on="order_date",
    right_on="date",
    how="left"
)

orders = orders.rename(columns={"date_key": "order_date_key"})
orders = orders.drop(columns=["date", "order_date"])

# -----------------------------------------
# 3️⃣ Join Customer Dimension
# -----------------------------------------

orders = orders.merge(
    customers[["customer_id", "customer_key"]],
    on="customer_id",
    how="left"
)

# -----------------------------------------
# 4️⃣ Aggregate Revenue From Line Fact
# -----------------------------------------

order_revenue = (
    order_items
    .groupby("order_id", as_index=False)
    .agg({
        "line_amount_eur": "sum",
        "quantity": "sum"
    })
)

orders = orders.merge(
    order_revenue,
    on="order_id",
    how="left"
)

orders["line_amount_eur"] = orders["line_amount_eur"].fillna(0)
orders["quantity"] = orders["quantity"].fillna(0)

orders = orders.rename(columns={
    "line_amount_eur": "total_order_amount_eur",
    "quantity": "total_quantity"
})

# -----------------------------------------
# 5️⃣ Final Fact Selection
# -----------------------------------------

fact_orders = orders[
    [
        "order_id",                 # degenerate dimension
        "order_date_key",
        "customer_key",
        "order_status",
        "currency",
        "total_quantity",
        "total_order_amount_eur"
    ]
]

fact_orders.to_parquet(GOLD_PATH, index=False)

print("fact_orders built successfully")
