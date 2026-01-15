#!/bin/bash

# Bluetooth Pairing Helper Script
echo "Scanning for Bluetooth devices... (5 seconds)"
bluetoothctl --timeout 5 scan on

echo "Available devices (Selection list):"
bluetoothctl devices

echo "Enter the MAC address of your Bluetooth headset/mic:"
read MAC

echo "Pairing with $MAC..."
bluetoothctl pair $MAC
bluetoothctl trust $MAC
bluetoothctl connect $MAC

echo "Testing connection..."
wpctl status | grep -A 5 "Sinks"
echo "If you see your device listed above, you are ready!"
