1️⃣ Linux SSH Brute Force Detection

index=linux_logs "Failed password"
| stats count by src_ip
| where count > 10

Meaning:

Detects more than 10 failed SSH login attempts from same IP
Possible brute force attack
--------------------------------------------------------------------
2️⃣ Windows Login Brute Force Detection
index=windows_logs EventCode=4625
| stats count by src_ip
| where count > 10

Meaning:

Detects many Windows login failures

Possible password brute force
------------------------------------------------------------------------
3️⃣ Successful Login After Many Failures
index=windows_logs (EventCode=4625 OR EventCode=4624)
| stats count by src_ip EventCode

Meaning:

Investigate when:

many 4625 events → then 4624

Possible account compromise after brute force.
----------------------------------------------------------------------
4️⃣ Privileged Account Login
index=windows_logs EventCode=4624
| search user IN ("admin","administrator","root")

Meaning:

Detects privileged account access

High-value accounts should always be monitored.
---------------------------------------------------------------------
5️⃣ Suspicious Login Time
index=windows_logs EventCode=4624
| eval hour=strftime(_time,"%H")
| where hour < 6 OR hour > 20

Meaning:

Detects logins outside business hours

Example flagged:

02:30 AM login
-----------------------------------------------------------------------
6️⃣ Firewall Port Scan Detection
index=firewall_logs
| stats count by src_ip dest_port
| where count > 50

Meaning:

One IP hitting many ports

Possible port scan / reconnaissance
-----------------------------------------------------------------------
7️⃣ DNS Suspicious Domain Frequency
index=dns_logs
| stats count by query
| where count > 100

Meaning:

Domain queried unusually often

Possible malware C2 communication
---------------------------------------------------------------------