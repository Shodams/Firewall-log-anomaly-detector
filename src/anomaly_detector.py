import pandas as pd
from sklearn.ensemble import IsolationForest
from risk_scoring import calculate_ip_risk

LOG_FILE = "sample_logs/firewall_logs.csv"

def run_ml_anomaly_detection(df):
    df_encoded = df.copy()

    df_encoded["action_code"] = df_encoded["action"].map({"allow": 0, "deny": 1})
    df_encoded["is_unknown_app"] = df_encoded["application"].str.contains("unknown", case=False, na=False).astype(int)
    df_encoded["is_risky_port"] = df_encoded["port"].isin([3389, 445, 4444, 23]).astype(int)
    df_encoded["is_restricted_zone"] = (df_encoded["destination_zone"] == "restricted").astype(int)

    features = df_encoded[[
        "port",
        "bytes",
        "action_code",
        "is_unknown_app",
        "is_risky_port",
        "is_restricted_zone"
    ]]

    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    df["ml_anomaly"] = model.fit_predict(features)
    df["ml_anomaly"] = df["ml_anomaly"].map({1: "Normal", -1: "Anomaly"})

    return df

def main():
    df = pd.read_csv(LOG_FILE)

    df = run_ml_anomaly_detection(df)
    risk_df = calculate_ip_risk(df)

    print("\nMachine Learning Anomaly Results")
    print("--------------------------------")
    print(df[df["ml_anomaly"] == "Anomaly"].head(20))

    print("\nTop Risky Source IPs")
    print("--------------------")
    print(risk_df.head(10))

     # Save outputs

    df[df["ml_anomaly"] == "Anomaly"].to_csv("output/anomalies.csv", index=False)

    risk_df.to_csv("output/risk_scores.csv", index=False)

    print("\nResults saved to /output folder")

if __name__ == "__main__":
    main()
