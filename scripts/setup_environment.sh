#!/usr/bin/env bash
#
# Full environment bootstrap for the ML platform on Raspberry Pi.

set -euo pipefail

PROJECT_ROOT="/home/pi/ml-pi-flow"
VENV_PATH="$PROJECT_ROOT/.venv"
ENV_FILE="$PROJECT_ROOT/.env"

# Ensure .env exists
if [[ ! -f "$ENV_FILE" ]]; then
  echo ".env file not found in $PROJECT_ROOT. Copy .env.example and fill in values."
  exit 1
fi

# Load environment variables safely
set -o allexport
source "$ENV_FILE"
set +o allexport

echo "📦 Updating package index..."
apt-get update -y

echo "🔧 Installing system packages..."
apt-get install -y docker.io docker-compose nginx certbot python3-venv

echo "👤 Adding 'pi' to docker group..."
usermod -aG docker pi

echo "🔌 Enabling & starting Docker service..."
systemctl enable docker
systemctl start docker

echo "🐍 Setting up Python virtual environment..."
if [[ ! -d "$VENV_PATH" ]]; then
  python3 -m venv "$VENV_PATH"
fi

echo "🐍 Activating virtual environment and installing Python dependencies..."
source "$VENV_PATH/bin/activate"
pip install --upgrade pip

pip install -r "$PROJECT_ROOT/dashboard/requirements.txt"
pip install fastapi uvicorn[standard] jinja2 python-multipart

deactivate

echo "▶️ Running systemd service installer..."
"$PROJECT_ROOT/scripts/install_systemd_service.sh"

echo "▶️ Running Nginx reverse proxy setup..."
"$PROJECT_ROOT/scripts/setup_reverse_proxy.sh"

echo "✅ Environment setup complete!"
echo "🔁 You may need to log out/in for docker group changes, or reboot."
