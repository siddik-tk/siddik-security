log_file = "/var/log/auth.log"

count = 0

with open(log_file) as f:
        for line in f:
                if "session opened for" in line or "Failed password" in line:
                        count += 1
                        print(line.strip())

print("\nTotal Failed Logins:", count)