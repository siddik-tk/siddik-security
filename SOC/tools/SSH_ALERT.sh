#!/bin/bash

# Easy-to-understand version
TIME_WINDOW=${1:-5}          # How many minutes to check
ALERT_THRESHOLD=${2:-6}      # How many attempts trigger alarm

echo "Looking for SSH attacks in last $TIME_WINDOW minutes..."
echo "Will alert if more than $ALERT_THRESHOLD failed attempts from same IP"
echo ""

# Get SSH logs → find failures → extract IPs → count → alert
sudo journalctl SYSLOG_IDENTIFIER=sshd --since "$TIME_WINDOW minutes ago" \
  | grep -E "Failed password|Invalid user" \
  | awk '{print $(NF-3)}' \
  | sort | uniq -c | sort -nr \
  | awk -v threshold=$ALERT_THRESHOLD '
    {
      if ($1 >= threshold)
        print "🚨 ALERT: " $1 " failed attempts from " $2
      else
        print "✅ Normal: " $1 " attempts from " $2
    }'