#!/bin/bash

# RPi 4 Offline Assistant Setup Script
# Run this on a fresh Raspberry Pi OS Lite (64-bit)

set -e

echo "--- Starting RPi 4 AI Assistant Setup ---"

# 1. Update System
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git alsa-utils libportaudio2 pipewire pipewire-audio-client-libraries bluez wireplumber

# 2. Setup Pipewire for Bluetooth
sudo cp /usr/share/doc/pipewire/examples/systemd/user/pipewire* /etc/systemd/user/
systemctl --user enable pipewire pipewire-pulse wireplumber

# 3. Install Ollama
echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh
# Start ollama and pull model
sudo systemctl enable ollama
ollama serve &
sleep 10
ollama pull tinyllama

# 4. Install Piper TTS
echo "Installing Piper..."
PIPER_VERSION="1.2.0"
wget https://github.com/rhasspy/piper/releases/download/v${PIPER_VERSION}/piper_arm64.tar.gz
sudo tar -C /usr/bin -xvf piper_arm64.tar.gz
mkdir -p ~/piper_models
wget -O ~/piper_models/en_US-lessac-medium.onnx https://github.com/rhasspy/piper/releases/download/v0.0.2/en_US-lessac-medium.onnx
wget -O ~/piper_models/en_US-lessac-medium.onnx.json https://github.com/rhasspy/piper/releases/download/v0.0.2/en_US-lessac-medium.onnx.json

# 5. Setup Python Environment
echo "Setting up Python environment..."
cd ~/offline_assistant
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install faster-whisper ollama sounddevice numpy requests

# 6. Create Systemd Service
echo "Creating assistant service..."
sudo bash -c "cat <<EOF > /etc/systemd/system/assistant.service
[Unit]
Description=Offline AI Assistant
After=network.target ollama.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/offline_assistant
Environment=\"PATH=/home/pi/offline_assistant/venv/bin\"
ExecStart=/home/pi/offline_assistant/venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable assistant.service

echo "--- Setup Complete! ---"
echo "Reboot your Pi, then use bluetoothctl to pair your headset."
echo "Your assistant will start automatically on boot."
