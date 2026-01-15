#!/bin/bash

# Nova OS Kiosk Setup Script
# Configures RPi 4 to boot directly into the AI Assistant GUI

set -e

echo "--- Configuring Kiosk Mode ---"

# 1. Install Kiosk Dependencies
sudo apt update
sudo apt install -y labwc chromium-browser seatd wayland-protocols

# 2. Create Autostart for Labwc (Wayland)
mkdir -p ~/.config/labwc
cat <<EOF > ~/.config/labwc/autostart
# Start Backend
cd ~/offline_assistant && source venv/bin/activate && python src/main.py &

# Start Browser in Kiosk Mode
chromium-browser --kiosk --noerrdialogs --disable-infobars --window-position=0,0 --window-size=1920,1080 http://localhost:8000
EOF

# 3. Configure Autologin to CLI
sudo raspi-config nonint do_boot_behaviour B2

# 4. Create .bash_profile to start labwc on login
cat <<EOF >> ~/.bash_profile
if [ -z "\$DISPLAY" ] && [ "\$(tty)" = "/dev/tty1" ]; then
  exec labwc
fi
EOF

# 5. Disable boot messages for a clean look
sudo sed -i 's/console=tty1/console=tty3 quiet loglevel=3 logo.nologo/' /boot/firmware/cmdline.txt

echo "--- Kiosk Configuration Complete ---"
echo "Please reboot to see the changes."
