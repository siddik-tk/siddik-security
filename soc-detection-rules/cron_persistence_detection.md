Title: Cron Persistence Detection

Description:
Detects cron jobs executing suspicious commands that may indicate persistence mechanisms used by attackers.

Detection Logic:
Cron execution logs containing suspicious commands such as curl, wget, bash, or netcat.

Splunk Rule:

index=linux sourcetype=syslog "CRON"
| search user=root
| stats count by host, _raw

# detect modification
index=linux sourcetype=audit "/etc/crontab"
| stats count by host, user, file

index=linux sourcetype=syslog "CRON"
| search user=root AND (" nc " OR "netcat")
| stats count by host, user

# prefered rule
index=linux sourcetype=syslog "CRON"
| search "curl" OR "wget" OR "nc" OR "bash"
| stats count by host, user

Severity:
High

MITRE ATT&CK Mapping:
T1053 – Scheduled Task/Job

False Positives:
- DevOps automation scripts
- System maintenance tasks
- Backup operations

Recommended Response:
- Inspect the cron entry
- Verify if the scheduled command is legitimate
- Remove malicious cron jobs