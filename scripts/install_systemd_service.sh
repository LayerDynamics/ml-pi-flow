#!/usr/bin/env bash
#
# Install and enable the ml-pi-flow.service systemd unit.

set -euo pipefail

SERVICE_FILE_CONTENT="[Unit]
Description=ML Platform Suite (Docker Compose)
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=true
WorkingDirectory=/home/pi/ml-pi-flow
EnvironmentFile=/home/pi/ml-pi-flow/.env
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
"

if [[ $EUID -ne 0 ]]; then
  echo "⚠️  Please run as root or via sudo."
  exit 1
fi

echo "📄 Writing systemd unit to /etc/systemd/system/ml-pi-flow.service..."
echo "$SERVICE_FILE_CONTENT" > /etc/systemd/system/ml-pi-flow.service

echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload

echo "✅ Enabling ml-pi-flow.service..."
systemctl enable ml-pi-flow.service

echo "🚀 Starting ml-pi-flow.service..."
systemctl start ml-pi-flow.service

echo "🎉 Systemd service installed, enabled, and started."
