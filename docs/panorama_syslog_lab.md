# Panorama Syslog Log Server Lab

## Goal

This lab simulates a real enterprise setup where Palo Alto Panorama forwards firewall logs to a centralized Linux syslog server. The collected logs can later be parsed by the Firewall Log Anomaly Detector.


## Lab Assumptions

| Item | Example |
|---|---|
| Log Server OS | Ubuntu Server |
| Log Server IP | 192.168.1.50 |
| Panorama IP | 192.168.1.10 |
| Syslog Protocol | UDP |
| Syslog Port | 514 |
| Log File | /var/log/panorama/panorama.log |

---

# Part 1: Build the Linux Syslog Server

## Step 1: Update Linux

```bash
sudo apt update
sudo apt upgrade -y
```

## Step 2: Install rsyslog

```bash
sudo apt install rsyslog -y
```

## Step 3: Enable and start rsyslog

```bash
sudo systemctl enable rsyslog
sudo systemctl start rsyslog
sudo systemctl status rsyslog
```

Expected result:

```text
active (running)
```

## Step 4: Create Panorama log directory

```bash
sudo mkdir -p /var/log/panorama
```

## Step 5: Set permissions

```bash
sudo chown syslog:adm /var/log/panorama
sudo chmod 750 /var/log/panorama
```

## Step 6: Create rsyslog config for Panorama

```bash
sudo nano /etc/rsyslog.d/10-panorama.conf
```

Paste this:

```conf
module(load="imudp")
input(type="imudp" port="514")

template(name="PanoramaLogFormat" type="string"
         string="/var/log/panorama/panorama.log")

if ($fromhost-ip == "192.168.1.10") then {
    action(type="omfile" dynaFile="PanoramaLogFormat")
    stop
}
```

Save:

```text
CTRL + O
ENTER
CTRL + X
```

## Step 7: Check rsyslog config syntax

```bash
sudo rsyslogd -N1
```

Expected result:

```text
rsyslogd: End of config validation run. Bye.
```

## Step 8: Restart rsyslog

```bash
sudo systemctl restart rsyslog
```

## Step 9: Allow UDP 514 through firewall

If using UFW:

```bash
sudo ufw allow 514/udp
sudo ufw reload
sudo ufw status
```

If using firewalld:

```bash
sudo firewall-cmd --add-port=514/udp --permanent
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

## Step 10: Confirm server is listening on UDP 514

```bash
sudo ss -lunp | grep 514
```

Expected result:

```text
udp   UNCONN   0   0   0.0.0.0:514
```

---

# Part 2: Test the Log Server Locally

## Step 1: Send a test syslog message

```bash
logger -n 127.0.0.1 -P 514 -d "PANORAMA TEST LOG: traffic allow trust to untrust"
```

## Step 2: Check the log file

```bash
sudo tail -f /var/log/panorama/panorama.log
```

Expected result:

```text
PANORAMA TEST LOG: traffic allow trust to untrust
```

Press:

```text
CTRL + C
```

to stop watching the file.

---

# Part 3: Configure Panorama to Send Logs

## Step 1: Create Syslog Server Profile

In Panorama:

```text
Panorama > Server Profiles > Syslog
```

Create a new profile:

| Field | Value |
|---|---|
| Name | SYSLOG-LINUX-SOC |
| Server Name | linux-syslog-01 |
| Syslog Server | 192.168.1.50 |
| Transport | UDP |
| Port | 514 |
| Format | BSD or IETF |
| Facility | LOG_USER |

## Step 2: Forward Firewall Traffic and Threat Logs

In Panorama:

```text
Objects > Log Forwarding
```

Create a new profile:

```text
Name: LF-SEND-TO-SYSLOG
```

Add match lists for:

```text
Traffic
Threat
URL
WildFire
Data Filtering
Tunnel
Authentication
```

For each log type:

```text
Filter: All Logs
Forward Method: Syslog
Syslog Profile: SYSLOG-LINUX-SOC
```

## Step 3: Attach Log Forwarding Profile to Security Policies

Go to:

```text
Policies > Security
```

For each security rule you want logged:

```text
Actions tab > Log Forwarding: LF-SEND-TO-SYSLOG
```

Also enable:

```text
Log at Session End
```

Recommended for most traffic rules:

```text
Log at Session End: Enabled
Log at Session Start: Optional
```

## Step 4: Forward Panorama System and Config Logs

Go to:

```text
Panorama > Log Settings
```

Configure forwarding for:

```text
System
Configuration
Threat
Traffic
Correlation
HIP Match
GlobalProtect
User-ID
```

Select:

```text
Syslog Profile: SYSLOG-LINUX-SOC
```

## Step 5: Commit Changes

In Panorama:

```text
Commit > Commit to Panorama
```

Then push to managed firewalls if required:

```text
Commit > Push to Devices
```

---

# Part 4: Verify Logs Are Arriving

On the Linux log server:

```bash
sudo tail -f /var/log/panorama/panorama.log
```

You should see logs arriving from Panorama.

To confirm packets are reaching the server:

```bash
sudo tcpdump -ni any udp port 514
```

Expected result:

```text
IP 192.168.1.10.XXXXX > 192.168.1.50.514: SYSLOG
```

---

# Part 5: Convert Syslog to CSV for the Detector

This project uses CSV logs for analysis.

Production systems usually normalize syslog using a SIEM, log collector, or parsing pipeline. In this project, the CSV represents normalized firewall logs.

Example fields:

```text
timestamp,source_ip,destination_ip,source_zone,destination_zone,application,port,action,bytes
```

Run the included synthetic log generator:

```bash
python generate_logs.py
```

Then run:

```bash
python src/anomaly_detector.py
```

Then launch the dashboard:

```bash
streamlit run dashboard/app.py
```

---

#  Notes

In a production environment:

- Use TCP or TLS syslog when possible.
- Restrict syslog access to Panorama/firewall IPs only.
- Store logs on dedicated storage.
- Rotate logs using logrotate.
- Forward logs into a SIEM such as Splunk, QRadar, Sentinel, Elastic, or Cortex XSIAM.
- Monitor disk usage.
- Use NTP so timestamps are accurate.
- Validate that all relevant security policies have logging enabled.
