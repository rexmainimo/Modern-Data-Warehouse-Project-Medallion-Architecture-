import pandas as pd
from pathlib import Path

WEB_EVENTS_PATH = "data/silver/web_events/web_events.parquet"
GOLD_PATH = "data/gold/facts/fact_web_events.parquet"

events = pd.read_parquet(WEB_EVENTS_PATH)
customers = pd.read_parquet(CUSTOMERS_PATH)
products = pd.read_parquet(PRODUCTS_PATH)
dates = pd.read_parquet(DATE_PATH)


events["event_date"] = pd.to_datetime(events["event_timestamp"]).dt.date

events = events.merge(
    dates[["date", "date_key"]],
    left_on="event_date",
    right_on="date",
    how="left"
)

events = events.rename(columns={"date_key": "event_date_key"})
events = events.drop(columns=["date"])

events = events.merge(
    customers[["customer_id", "customer_key"]],
    on="customer_id",
    how="left"
)

events = events.merge(
    products[["product_id", "product_key"]],
    on="product_id",
    how="left"
)

events["event_count"] = 1

fact_web_events = events[
    [
        "event_id",
        "event_date_key",
        "customer_key",
        "product_key",
        "session_id",
        "event_type",
        "page_url",
        "event_count"
    ]
]

fact_web_events.to_parquet(GOLD_PATH, index=False)
print("fact_web_events built successfully")
