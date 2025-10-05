#!/bin/bash

interface="eth0"

echo "=== Simple Network Monitor ==="
echo "Monitoring interface: $interface"
echo ""


check_traffic() {

    start_bytes=$(cat /sys/class/net/$interface/statistics/tx_bytes)

    echo "Monitoring for 10 seconds..."
    sleep 10


    end_bytes=$(cat /sys/class/net/$interface/statistics/tx_bytes)


    traffic=$((end_bytes - start_bytes))

    echo "Data sent in 10 seconds: $traffic bytes"


    if [ $traffic -gt 1000000 ]; then
        echo "🚨 ALERT: High network activity! (>1MB in 10s)"
        echo "Possible data exfiltration!"
    elif [ $traffic -gt 50000 ]; then
        echo "⚠️  Warning: Moderate network activity"
    else
        echo "✅ Normal network activity"
    fi
}


show_stats() {
    echo ""
    echo "=== Current Statistics ==="
    echo "Bytes Sent: $(cat /sys/class/net/$interface/statistics/tx_bytes)"
    echo "Bytes Received: $(cat /sys/class/net/$interface/statistics/rx_bytes)"
    echo "Packets Sent: $(cat /sys/class/net/$interface/statistics/tx_packets)"
    echo "Packets Received: $(cat /sys/class/net/$interface/statistics/rx_packets)"
}


while true; do
    echo ""
    echo "Choose an option:"
    echo "1) Check traffic for 10 seconds"
    echo "2) Show current statistics"
    echo "3) Exit"
    echo ""
    read -p "Enter choice (1-3): " choice

    case $choice in
        1)
            check_traffic
            ;;
        2)
            show_stats
            ;;
        3)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please enter 1, 2, or 3."
            ;;
    esac
done