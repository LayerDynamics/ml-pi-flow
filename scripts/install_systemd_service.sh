#!/usr/bin/env bash
#
# Install and enable the ml-pi-flow.service systemd unit.

set -euo pipefail

SERVICE_NAME="ml-pi-flow"
SERVICE_PATH=/etc/systemd/system/${SERVICE_NAME}.service
WORKING_DIR="/home/pi/ml-pi-flow"
COMPOSE_BIN="/usr/bin/docker-compose"

if [[ $EUID -ne 0 ]]; then
  echo "⚠️  Please run as root or via sudo."
  exit 1
fi

echo "📄 Writing systemd unit to ${SERVICE_PATH}..."
cat > ${SERVICE_PATH} <<EOF
[Unit]
Description=ML Platform Suite (Docker Compose)
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=true
WorkingDirectory=${WORKING_DIR}
EnvironmentFile=${WORKING_DIR}/.env
ExecStart=${COMPOSE_BIN} up -d
ExecStop=${COMPOSE_BIN} down
TimeoutStartSec=0
User=pi
Group=pi

[Install]
WantedBy=multi-user.target
EOF

echo "🔄 Reloading systemd daemon..."
systemctl daemon-reload

echo "✅ Enabling ${SERVICE_NAME}.service..."
systemctl enable ${SERVICE_NAME}.service

echo "🚀 Starting ${SERVICE_NAME}.service..."
systemctl start ${SERVICE_NAME}.service

echo "🎉 Systemd service installed, enabled, and started."
