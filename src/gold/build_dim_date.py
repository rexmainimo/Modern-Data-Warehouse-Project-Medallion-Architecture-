import pandas as pd
from pathlib import Path


ORDERS_PATH = "data/silver/orders/orders.parquet"
GOLD_PATH = "data/gold/dimensions/dim_date.parquet"

Path(GOLD_PATH).parent.mkdir(parents=True, exist_ok=True)


orders = pd.read_parquet(ORDERS_PATH)

min_date = orders["order_date"].min()
max_date = orders["order_date"].max()

# Safety buffer
start_date = pd.to_datetime(min_date) - pd.Timedelta(days=30)
end_date = pd.to_datetime(max_date) + pd.Timedelta(days=30)

# Generate date range
dates = pd.date_range(start=start_date, end=end_date, freq="D")

df = pd.DataFrame({"date": dates})

df["date_key"] = df["date"].dt.strftime("%Y%m%d").astype(int)


df["year"] = df["date"].dt.year
df["quarter"] = df["date"].dt.quarter
df["month"] = df["date"].dt.month
df["month_name"] = df["date"].dt.month_name()
df["day"] = df["date"].dt.day
df["day_of_week"] = df["date"].dt.weekday + 1
df["day_name"] = df["date"].dt.day_name()
df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
df["is_weekend"] = df["day_of_week"].isin([6, 7])

# Reorder columns
df = df[
    [
        "date_key",
        "date",
        "year",
        "quarter",
        "month",
        "month_name",
        "day",
        "day_of_week",
        "day_name",
        "week_of_year",
        "is_weekend"
    ]
]

df.to_parquet(GOLD_PATH, index=False)

print("dim_date built successfully")
