#!/usr/bin/env bash
#
# Install and enable the ml_platform.service systemd unit.

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
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
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

echo "📄 Writing systemd unit to /etc/systemd/system/ml_platform.service..."
cat > /etc/systemd/system/ml_platform.service <<EOF
$SERVICE_FILE_CONTENT
EOF

echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload

echo "✅ Enabling ml_platform.service..."
systemctl enable ml_platform.service

echo "🚀 Starting ml_platform.service..."
systemctl start ml_platform.service

echo "🎉 Systemd service installed, enabled, and started."
