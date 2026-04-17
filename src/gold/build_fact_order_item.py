import pandas as pd
from pathlib import Path
import pandas as pd
from pathlib import Path

# Paths
ORDER_ITEMS_PATH = "data/silver/orderItems/orderItems.parquet"
ORDERS_PATH = "data/silver/orders/orders.parquet"
CUSTOMERS_PATH = "data/gold/dimensions/dim_customers.parquet"   
PRODUCTS_PATH = "data/gold/dimensions/dim_products.parquet"
DATE_PATH = "data/gold/dimensions/dim_date.parquet"
FX_PATH = "data/silver/exchange_rates/exchange_rates.parquet"

GOLD_PATH = "data/gold/facts/fact_order_items.parquet"
Path(GOLD_PATH).parent.mkdir(parents=True, exist_ok=True)

# -----------------------------------------
# Load data
# -----------------------------------------

order_items = pd.read_parquet(ORDER_ITEMS_PATH)
orders = pd.read_parquet(ORDERS_PATH)
customers = pd.read_parquet(CUSTOMERS_PATH)
products = pd.read_parquet(PRODUCTS_PATH)
dates = pd.read_parquet(DATE_PATH)
fx = pd.read_parquet(FX_PATH)

# -----------------------------------------
# 1️⃣ Join Orders (to get customer + date)
# -----------------------------------------

order_items = order_items.merge(
    orders[["order_id", "customer_id", "order_date", "currency"]],
    on="order_id",
    how="left"
)

# -----------------------------------------
# 2️⃣ Join Customer Dimension
# -----------------------------------------

order_items = order_items.merge(
    customers[["customer_id", "customer_key"]],
    on="customer_id",
    how="left"
)

# -----------------------------------------
# 3️⃣ Join Product Dimension
# -----------------------------------------

order_items = order_items.merge(
    products[["product_id", "product_key"]],
    on="product_id",
    how="left"
)

# -----------------------------------------
# 4️⃣ Join Date Dimension
# -----------------------------------------

order_items["order_date"] = pd.to_datetime(
    order_items["order_date"]
)

dates["date"] = pd.to_datetime(dates["date"])


order_items = order_items.merge(
    dates[["date", "date_key"]],
    left_on="order_date",
    right_on="date",
    how="left"
)

order_items = order_items.rename(
    columns={"date_key": "order_date_key"}
).drop(columns=["date"])

# -----------------------------------------
# 5️⃣ Revenue Calculations
# -----------------------------------------

order_items["line_amount_local"] = (
    order_items["quantity"] * order_items["unit_price"]
)

# FX join (convert to EUR)
# Ensure both sides are datetime64[ns]
order_items["order_date"] = pd.to_datetime(order_items["order_date"])
fx["date"] = pd.to_datetime(fx["date"])

order_items = order_items.merge(
    fx[["source_currency", "date", "rate"]],
    left_on=["currency", "order_date"],
    right_on=["source_currency", "date"],
    how="left"
)


order_items["line_amount_eur"] = (
    order_items["line_amount_local"] / order_items["rate"]
)

# -----------------------------------------
# 6️⃣ Select Fact Columns
# -----------------------------------------

fact_order_items = order_items[
    [
        "order_item_id",     # degenerate dimension
        "order_id",
        "customer_key",
        "product_key",
        "order_date_key",
        "quantity",
        "unit_price",
        "line_amount_local",
        "line_amount_eur"
    ]
]

fact_order_items = fact_order_items.dropna(
    subset=["customer_key", "product_key", "order_date_key"]
)

# -----------------------------------------
# 7️⃣ Save
# -----------------------------------------

fact_order_items.to_parquet(GOLD_PATH, index=False)

print("fact_order_items built successfully")
