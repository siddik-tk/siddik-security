import re

pattern = r"\d+\.\d+\.\d+\.\d+"

log_file = r"C:\Users\mdsid\Documents\siddik-security\SOC\auth.log"

count = 0

with open(log_file) as f:
        for line in f:
                if "session opened for" in line or "Failed password" in line:
                        count += 1
                        #print(line.strip())
                        match = re.search(pattern, line)
                        ip = match.group() if match else "No IP found"
                        timestamp = " ".join(line.split()[0:3])
                        print(f"{timestamp} -> Failed password from {ip}")

print("\nTotal Failed Logins:", count)