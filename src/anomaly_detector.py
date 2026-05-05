import pandas as pd

LOG_FILE = "sample_logs/firewall_logs.csv"

def detect_denied_traffic_spike(df, threshold=3):
    denied = df[df["action"] == "deny"]
    counts = denied.groupby("source_ip").size()

    alerts = []
    for source_ip, count in counts.items():
        if count >= threshold:
            alerts.append({
                "alert": "Denied traffic spike",
                "source_ip": source_ip,
                "count": count,
                "severity": "Medium"
            })

    return alerts

def detect_unusual_ports(df):
    risky_ports = [3389, 4444, 23, 445]
    suspicious = df[df["port"].isin(risky_ports)]

    alerts = []
    for _, row in suspicious.iterrows():
        alerts.append({
            "alert": "Risky destination port detected",
            "source_ip": row["source_ip"],
            "destination_ip": row["destination_ip"],
            "port": row["port"],
            "application": row["application"],
            "severity": "High"
        })

    return alerts

def main():
    df = pd.read_csv(LOG_FILE)

    alerts = []
    alerts.extend(detect_denied_traffic_spike(df))
    alerts.extend(detect_unusual_ports(df))

    print("\nFirewall Log Anomaly Detector Results")
    print("------------------------------------")

    if not alerts:
        print("No anomalies detected.")
    else:
        for alert in alerts:
            print(alert)

if __name__ == "__main__":
    main()
