import pandas as pd
from pathlib import Path

BRONZE_FIXED_PATH = "/opt/airflow/data/bronze_fixed/exchange_rates/exchange_rates_fixed.parquet"
SILVER_PATH = "/opt/airflow/data/silver/exchange_rates/exchange_rates.parquet"

def main():
    Path(SILVER_PATH).parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(BRONZE_FIXED_PATH)

    # -------------------------------------------
    # Remove duplicates
    # -------------------------------------------

    df = df.drop_duplicates(
        subset=["source_currency", "target_currency", "date"],
        keep="last"
    )

    # -------------------------------------------
    # Keep only business columns
    # -------------------------------------------

    df = df[[
        "source_currency",
        "target_currency",
        "date",
        "rate"
    ]]

    df.to_parquet(SILVER_PATH, index=False)

    print("Silver exchange_rates written successfully")


if __name__ == "__main__":
    main()
