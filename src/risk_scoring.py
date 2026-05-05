import pandas as pd

def calculate_ip_risk(df):
    risk_scores = {}

    for source_ip, group in df.groupby("source_ip"):
        score = 0

        denied_count = len(group[group["action"] == "deny"])
        risky_ports = group[group["port"].isin([3389, 445, 4444, 23])]
        unknown_apps = group[group["application"].str.contains("unknown", case=False, na=False)]
        restricted_access = group[group["destination_zone"] == "restricted"]

        score += denied_count * 5
        score += len(risky_ports) * 10
        score += len(unknown_apps) * 8
        score += len(restricted_access) * 12

        if score >= 80:
            severity = "Critical"
        elif score >= 50:
            severity = "High"
        elif score >= 25:
            severity = "Medium"
        else:
            severity = "Low"

        risk_scores[source_ip] = {
            "source_ip": source_ip,
            "risk_score": score,
            "severity": severity,
            "denied_count": denied_count,
            "risky_port_events": len(risky_ports),
            "unknown_app_events": len(unknown_apps),
            "restricted_zone_events": len(restricted_access)
        }

    return pd.DataFrame(risk_scores.values()).sort_values(by="risk_score", ascending=False)
