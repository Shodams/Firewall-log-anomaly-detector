import pandas as pd
import random
from datetime import datetime, timedelta

# Config
NUM_LOGS = 1000

source_ips = [f"10.10.{i}.{j}" for i in range(1, 50) for j in range(1, 10)]
dest_ips = [f"172.16.{i}.{j}" for i in range(1, 20) for j in range(1, 10)]

zones = ["trust", "untrust", "dmz", "restricted"]
apps = ["web-browsing", "ssl", "dns", "ssh", "rdp", "unknown-tcp", "unknown-udp"]
ports = [80, 443, 53, 22, 3389, 4444, 445]
actions = ["allow", "deny"]

start_time = datetime(2026, 1, 1)

logs = []

for i in range(NUM_LOGS):
    timestamp = start_time + timedelta(seconds=random.randint(0, 86400))
    # Inject anomaly (5% of logs)
    if random.random() < 0.05:
        log["source_ip"] = "10.10.99.99"
        log["port"] = 3389
        log["action"] = "deny"
    log = {
        "timestamp": timestamp,
        "source_ip": random.choice(source_ips),
        "destination_ip": random.choice(dest_ips),
        "source_zone": random.choice(zones),
        "destination_zone": random.choice(zones),
        "application": random.choice(apps),
        "port": random.choice(ports),
        "action": random.choices(actions, weights=[0.7, 0.3])[0],  # more allow than deny
        "bytes": random.randint(50, 10000)
    }

    logs.append(log)

df = pd.DataFrame(logs)

# Save file
df.to_csv("sample_logs/firewall_logs.csv", index=False)

print("Generated 1000 firewall log entries!")
