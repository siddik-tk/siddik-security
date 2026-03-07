# SOC Bruteforce Detector

A Python-based SOC automation tool that detects SSH brute-force attacks from Linux authentication logs (`auth.log`).  
The script analyzes failed login attempts, identifies suspicious activity within a time window, enriches attacker IPs with threat intelligence, and generates alerts.

This project demonstrates core SOC detection engineering concepts including log parsing, event correlation, IOC enrichment, and alert tuning.

---

## Features

- Parses Linux `auth.log` files
- Extracts attacker IP addresses using regex
- Detects SSH brute-force attacks based on time-window logic
- Filters internal/private network traffic to reduce false positives
- Enriches attacker IPs with threat intelligence (country and ISP)
- Generates clean SOC-style alerts

---

## Detection Logic

The detection pipeline follows a typical SOC workflow:


Detection rule used:

- **≥4 failed login attempts**
- **within 60 seconds**
- **from the same IP**

Internal/private networks are ignored to reduce noise.

Filtered ranges include:

- `127.0.0.0/8`
- `10.0.0.0/8`
- `192.168.0.0/16`
- trusted infrastructure IPs

---

## Example Log Entry

- ref the sample auth.log file. // you should give you system log file in production


The script extracts:

- attacker IP
- timestamp
- event type

---

## Example Output

PS C:\Users\<user>> python Bruteforce_Detector_v1.py

⚠ SSH BRUTE FORCE DETECTED
IP: 185.34.22.90
Attempts: 5
Time Window: 13 seconds
Country: Russia
ISP: LTD "Erline"

⚠ SSH BRUTE FORCE DETECTED
IP: 91.23.55.12
Attempts: 4
Time Window: 12 seconds
Country: Germany
ISP: Deutsche Telekom AG


---

## Installation

Clone the repository:

```bash
git clone https://github.com/siddik-tk/siddik-security/tree/master/SOC-Bruteforce-Detector
cd SOC-Bruteforce-Detector
