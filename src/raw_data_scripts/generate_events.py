# generate_events.py
import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

NUM_EVENTS = 500_000
EVENT_TYPES = ["page_view", "add_to_cart", "checkout"]

events = []

start_time = datetime.now() - timedelta(days=30)

for event_id in range(1, NUM_EVENTS + 1):
    event_type = random.choices(
        EVENT_TYPES,
        weights=[0.7, 0.2, 0.1]
    )[0]

    event = {
        "event_id": event_id,
        "event_type": event_type,
        "customer_id": random.randint(1, 10_000),
        "product_id": random.randint(1, 1_000) if event_type != "page_view" else None,
        "session_id": fake.uuid4(),
        "event_timestamp": (
            start_time + timedelta(seconds=random.randint(0, 2_592_000))
        ).isoformat()
    }

    events.append(event)

# Write as JSON Lines (very realistic)
with open("output/web_events.json", "w") as f:
    for event in events:
        f.write(json.dumps(event) + "\n")
