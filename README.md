# Firewall Log Anomaly Detector

## Overview

This project detects anomalies in firewall traffic and threat logs. It is inspired by enterprise firewall operations involving Palo Alto Panorama, centralized logging, Zero Trust segmentation, SSL decryption visibility, and SOC monitoring workflows.

The detector reviews firewall log activity and identifies suspicious behavior such as unusual source IP activity, denied traffic spikes, abnormal destination patterns, risky application usage, and potential policy violations.

## Why This Project Matters

Enterprise security teams rely on centralized firewall logs to detect threats, investigate incidents, and validate policy enforcement. This project simulates that workflow by analyzing firewall logs and flagging unusual activity for security review.

## Skills Demonstrated

- Firewall log analysis
- Zero Trust security monitoring
- Network segmentation visibility
- Threat detection logic
- SOC-style alerting
- Python scripting
- Security analytics
- GitHub documentation
- Architecture diagramming

## Architecture

```mermaid
flowchart LR
    A[Firewall Devices] --> B[Panorama / Centralized Log Forwarding]
    B --> C[Syslog / Log Pipeline]
    C --> D[Firewall Log Parser]
    D --> E[Anomaly Detection Engine]
    E --> F[Alert Output]
    F --> G[SOC Analyst Review]
```

## Detection Logic

The project can detect:

- High volume of denied traffic from one source
- Repeated access attempts to restricted zones
- Suspicious traffic outside normal business hours
- Unusual destination ports
- High-risk application activity
- Potential command-and-control behavior
- Unexpected traffic between segmented zones

## Example Workflow

```mermaid
sequenceDiagram
    participant FW as Firewall
    participant SYS as Syslog Pipeline
    participant APP as Anomaly Detector
    participant SOC as SOC Analyst

    FW->>SYS: Send traffic and threat logs
    SYS->>APP: Forward normalized logs
    APP->>APP: Analyze patterns
    APP->>SOC: Generate anomaly alert
    SOC->>SOC: Investigate source, destination, app, and policy
```

## Sample Alert

```text
ALERT: Unusual denied traffic spike detected
Source IP: 10.10.25.44
Destination Zone: DMZ
Action: deny
Reason: Source exceeded normal denied-traffic threshold
Severity: Medium
```

## How To Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the detector:

```bash
python src/anomaly_detector.py
```

## Future Improvements

- Add machine learning-based anomaly detection
- Integrate with SIEM tools
- Add dashboard visualizations
- Support Palo Alto traffic, threat, URL, and WildFire logs
- Add MITRE ATT&CK mapping
- Add risk scoring by source IP, application, and zone

## Resume Bullet

Built a firewall log anomaly detector that analyzes centralized firewall logs to identify suspicious network behavior, denied traffic spikes, risky application usage, and potential policy violations in support of SOC monitoring and Zero Trust enforcement.
