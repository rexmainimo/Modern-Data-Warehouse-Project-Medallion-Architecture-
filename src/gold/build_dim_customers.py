import pandas as pd
from pathlib import Path

SILVER_PATH = "/opt/airflow/data/silver/customers/customers.parquet"
GOLD_PATH = "/opt/airflow/data/gold/dimensions/dim_customers.parquet"

def main():
    Path(GOLD_PATH).parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_parquet(SILVER_PATH)

    df = df.sort_values('customer_id').reset_index(drop=True)
    df['customer_key'] = df.index + 1

    dim_customers = df[
        [
            "customer_key",
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "country",
            "signup_date"
        ]
    ]

    dim_customers.to_parquet(GOLD_PATH, index=False)

    print("dim_customers built successfully")



if __name__ == "__main__":
    main()