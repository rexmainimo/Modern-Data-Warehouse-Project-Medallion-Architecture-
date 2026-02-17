import requests
import csv
from datetime import date
import os

ECB_URL = "https://api.frankfurter.app/latest"

params = {
    "from": "EUR",
    "to": "USD,GBP,CHF"
}

response = requests.get(ECB_URL, params=params)
data = response.json()

file_exists = os.path.isfile("output/exchange_rates.csv")

with open("output/exchange_rates.csv", "a", newline="") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow([
            "rate_date",
            "base_currency",
            "target_currency",
            "exchange_rate"
        ])

    for currency, rate in data["rates"].items():
        writer.writerow([
            data["date"],
            data["base"],
            currency,
            rate
        ])