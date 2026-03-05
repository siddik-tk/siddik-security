Title: SSH Brute Force Detection

Detection Logic:
Detect multiple failed SSH login attempts from the same IP within a short time window.

Splunk Rule:

index=linux sourcetype=auth "Failed password"
| stats count by src_ip, user
| where count >= 5
| sort - count

index=linux sourcetype=auth "Failed password"
| bucket _time span=5m
| stats count by _time, src_ip, user
| where count >= 5

index=linux sourcetype=auth ("Failed password" OR "Accepted password")
| eval event_type=if(searchmatch("Failed password"),"fail","success")
| stats count(eval(event_type="fail")) as fail_count,
        count(eval(event_type="success")) as success_count
        by src_ip, user
| where fail_count >= 5 AND success_count >= 1

... 
| where NOT cidrmatch("10.0.0.0/8", src_ip)
| where src_ip != "192.168.1.100"

#prefered rule

index=linux sourcetype=auth "Failed password"
| bucket _time span=5m
| stats count by _time, src_ip, user
| where count >= 5

False Positives:
- User mistyped password
- Internal security scans
- Automated scripts