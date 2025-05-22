#!/usr/bin/env bash
#
# Full environment bootstrap for the ML platform on Raspberry Pi.

set -euo pipefail

# Ensure .env is present
if [[ ! -f /home/pi/ml-pi-flow/.env ]]; then
  echo ".env file not found in /home/pi/ml-pi-flow. Copy .env.example and fill in values."
  exit 1
fi

# Load environment vars
export $(grep -v '^#' /home/pi/ml-pi-flow/.env | xargs)

echo "📦 Updating package index..."
apt-get update -y

echo "🔧 Installing system packages..."
apt-get install -y docker.io docker-compose nginx certbot python3-pip

echo "👤 Adding 'pi' to docker group..."
usermod -aG docker pi

echo "🔌 Enabling & starting Docker service..."
systemctl enable docker
systemctl start docker

echo "🐍 Installing Python dependencies for dashboard and portal..."
pip3 install --upgrade pip
pip3 install -r /home/pi/ml-pi-flow/dashboard/requirements.txt
pip3 install fastapi uvicorn[standard] jinja2 python-multipart

echo "▶️ Running systemd service installer..."
/home/pi/ml-pi-flow/scripts/install_systemd_service.sh

echo "▶️ Running Nginx reverse proxy setup..."
/home/pi/ml-pi-flow/scripts/setup_reverse_proxy.sh

echo "✅ Environment setup complete!"
echo "🔁 You may need to log out/in for docker group changes, or reboot."
