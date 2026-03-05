Title: DNS Anomaly Detection

Description:
Detects suspicious DNS queries that may indicate DNS tunneling or command-and-control communication.

Detection Logic:
DNS queries containing unusually long domain names.

Splunk Rule:

# High DNS Volume
index=dns sourcetype=dns
| stats count by src_ip, query
| where count > 100

# by long domain name
index=dns sourcetype=dns
| eval len=len(query)
| where len > 60
| stats count by src_ip, query

# Detect Rare Domains
index=dns sourcetype=dns
| stats count by query
| where count < 3

Severity:
Medium

MITRE ATT&CK Mapping:
T1071 – Application Layer Protocol

False Positives:
- Content Delivery Networks (CDNs)
- Software update services
- Antivirus telemetry

Recommended Response:
- Inspect queried domain
- Check domain reputation
- Investigate host generating the queries