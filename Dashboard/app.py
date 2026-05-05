import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from anomaly_detector import run_ml_anomaly_detection
from risk_scoring import calculate_ip_risk

st.set_page_config(page_title="Firewall Mini SIEM", layout="wide")

st.title("Firewall Log Anomaly Detector - Mini SIEM Dashboard")

df = pd.read_csv("sample_logs/firewall_logs.csv")
df = run_ml_anomaly_detection(df)
risk_df = calculate_ip_risk(df)

total_logs = len(df)
total_anomalies = len(df[df["ml_anomaly"] == "Anomaly"])
denied_logs = len(df[df["action"] == "deny"])
critical_ips = len(risk_df[risk_df["severity"] == "Critical"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Logs", total_logs)
col2.metric("ML Anomalies", total_anomalies)
col3.metric("Denied Sessions", denied_logs)
col4.metric("Critical IPs", critical_ips)

st.subheader("Top Risky Source IPs")
st.dataframe(risk_df.head(15), use_container_width=True)

st.subheader("Anomaly Events")
st.dataframe(df[df["ml_anomaly"] == "Anomaly"], use_container_width=True)

st.subheader("Traffic by Action")
fig_action = px.histogram(df, x="action", title="Allow vs Deny Traffic")
st.plotly_chart(fig_action, use_container_width=True)

st.subheader("Risk Score by Source IP")
fig_risk = px.bar(risk_df.head(10), x="source_ip", y="risk_score", color="severity")
st.plotly_chart(fig_risk, use_container_width=True)

st.subheader("Traffic by Destination Zone")
fig_zone = px.histogram(df, x="destination_zone")
st.plotly_chart(fig_zone, use_container_width=True)
