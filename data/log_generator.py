import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

num_logs = 100000

users = [f"user_{i}" for i in range(1, 501)]

ips = [f"192.168.{i}.{j}" for i in range(1, 20) for j in range(1, 50)]

locations = ["India", "USA", "Japan", "Germany", "UK", "Singapore"]

event_types = [
    "login_success",
    "login_failure",
    "file_access",
    "password_change",
    "unauthorized_access",
    "privilege_escalation"
]

attack_events = [
    "login_failure",
    "unauthorized_access",
    "privilege_escalation"
]

logs = []

start_time = datetime.now() - timedelta(days=30)

for i in range(num_logs):

    timestamp = start_time + timedelta(seconds=random.randint(0, 2592000))

    user = random.choice(users)

    ip = random.choice(ips)

    location = random.choice(locations)

    if random.random() < 0.95:
        event = random.choice(event_types[:4])
        label = "normal"
    else:
        event = random.choice(attack_events)
        label = "attack"

    logs.append([
        timestamp,
        user,
        ip,
        location,
        event,
        label
    ])

df = pd.DataFrame(logs, columns=[
    "timestamp",
    "user_id",
    "ip_address",
    "location",
    "event_type",
    "label"
])

df = df.sort_values("timestamp")

df.to_csv("data/raw_logs.csv", index=False)

print("Log dataset generated successfully")
print("Total logs:", len(df))
print(df.head())
