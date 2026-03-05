Title: Reverse Shell Detection

Description:
Detects outbound connections initiated by shell processes which may indicate reverse shell activity.

Detection Logic:
Shell processes making outbound connections to high or unusual ports.

Splunk Rule:

# Process-Based Detection (Linux logs / auditd)
index=linux sourcetype=process ("nc" OR "bash" OR "python")
| search "-e" OR "/dev/tcp"
| stats count by host, process, user

# Network-Based Detection (Best L1 Approach)
index=linux sourcetype=netflow direction=outbound
| where dest_port > 1024
| stats count by host, dest_ip, dest_port

# ESTABLISHED Shell Detection (ss equivalent)
index=linux sourcetype=netstat state=ESTABLISHED
| search process="bash" OR process="nc"
| stats count by host, dest_ip

# prefered rule
index=linux sourcetype=netflow
| where dest_port > 1024
| search process="bash"
| stats count by host, dest_ip, dest_port

index=linux sourcetype=netflow
| where dest_port=4444
| where NOT cidrmatch("10.0.0.0/8", dest_ip)
| search process="bash"
| stats count by host, dest_ip, dest_port

Severity:
High

MITRE ATT&CK Mapping:
T1071 – Application Layer Protocol

False Positives:
- Administrative SSH tunneling
- Automation scripts making external connections
- Monitoring agents

Recommended Response:
- Inspect the process initiating the connection
- Verify destination IP
- Kill suspicious processes and isolate host if needed