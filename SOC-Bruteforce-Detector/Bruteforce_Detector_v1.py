import re
import requests

pattern = r"\d+\.\d+\.\d+\.\d+"

log_file = r"C:\Users\mdsid\Documents\siddik-security\SOC\auth.log"

import os

def block_ip(ip):

    print(f"[ACTION] Blocking attacker IP: {ip}")
    os.system(f"iptables -A INPUT -s {ip} -j DROP")

def enrich_ip(ip):

    url = "http://ip-api.com/json/" + ip

    response = requests.get(url)

    data = response.json()

    country = data.get("country", "Unknown")
    isp = data.get("isp", "Unknown")

    return country, isp

def follow_log(file):

    file.seek(0, 2)

    while True:
        line = file.readline()

        if not line:
            continue

        yield line

def extract_ip(line):
    match = re.search(pattern, line)
    return match.group() if match else "No IP found"

def parse_logs():

    attempts = {}
    remote_server_ips = ["101.18.1.71"]

    with open(log_file) as f:
        for line in follow_log(f):
                    if "Failed password" in line:
                            #print(line.strip())
                            ip = extract_ip(line)
                            if ip.startswith("192.168") or ip.startswith("10.") or ip.startswith("172.16"):
                                    continue
                            if ip in remote_server_ips:
                                    continue
                            timestr = line.split()[2]
                            h,m,s = timestr.split(":")
                            seconds = int(h)*3600 + int(m)*60 + int(s)
                            if ip not in attempts:
                                    attempts[ip] = [seconds]
                            else:
                                    attempts[ip].append(seconds)

    return attempts
                            #timestamp = " ".join(line.split()[0:3])


def detect_bruteforce(attempts):
    for ip, times in attempts.items():
            if len(times) > 3:
                    times.sort()
                    if max(times) - min(times) <= 60:
                            country, isp = enrich_ip(ip)
                            print("\n⚠ SSH BRUTE FORCE DETECTED")
                            print("IP:", ip)
                            print("Attempts:", len(times))
                            print("Time Window:", max(times)-min(times), "seconds")
                            print("Country:", country)
                            print("ISP:", isp)
                            block_ip(ip)

def main():

    attempts = parse_logs()
    detect_bruteforce(attempts)

if __name__ == "__main__":
    main()