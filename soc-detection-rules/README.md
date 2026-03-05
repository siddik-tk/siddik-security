Project: SOC Detection Rules

Overview:
This repository contains detection engineering rules designed for Security Operations Center (SOC) environments. The rules detect common attacker behaviors using Linux logs and Splunk queries.

Detection Rules Included:
- SSH Brute Force Detection
- Cron Persistence Detection
- Reverse Shell Detection
- SUID Privilege Escalation Detection
- DNS Anomaly Detection

Data Sources:
- Linux Authentication Logs (auth.log)
- Syslog
- Process Monitoring Logs
- Netflow Logs
- DNS Logs

Objective:
Demonstrate behavioral detection techniques used by SOC analysts to identify attacks across multiple stages of the attacker lifecycle.

MITRE ATT&CK Coverage:
The detection rules align with common adversary tactics including brute force, persistence, command-and-control, privilege escalation, and network anomalies.

# all my learning rules for later usage and revision is here. Anyone can use this rules for their work.