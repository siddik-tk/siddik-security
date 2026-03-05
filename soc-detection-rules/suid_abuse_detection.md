Title: SUID Abuse Detection

Description:
Detects potential privilege escalation attempts by identifying processes executed with effective root privileges by non-root users.

Detection Logic:
Processes executed where the real user is not root but effective UID equals root.

Splunk Rule:

# Detect Permission Change to SUID
index=linux sourcetype=audit "chmod"
| search "4755" OR "+s"
| stats count by host, user, file

# Detect New SUID Binary in /tmp
index=linux sourcetype=audit
| search file="/tmp/*" AND perm="4000"
| stats count by host, file

# Detect Execution of Suspicious SUID Binary
index=linux sourcetype=process
| search user!=root euid=0
| stats count by host, user, process

Severity:
High

MITRE ATT&CK Mapping:
T1548 – Abuse Elevation Control Mechanism

False Positives:
- Legitimate SUID binaries such as passwd or sudo
- System administration tasks

Recommended Response:
- Verify the executed binary
- Check for newly created SUID files
- Investigate user activity leading to privilege escalation