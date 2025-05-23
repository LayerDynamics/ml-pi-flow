# ML PI Flow Suite

## Prerequisites
- Docker & Docker Compose
- Python 3.9+ (for dashboard & portal)

## Setup
1. Copy `.env.example` → `.env` and fill in secrets.
2. Build & start everything:
   ```bash
   docker-compose up -d --build


Based on your nginx config and Docker Compose setup, you can access your services through the reverse proxy using your Raspberry Pi's IP address (replace `192.168.124.169` with your actual IP if different) and the mapped port (default is 80 inside the container, but check your host mapping—commonly `8880` or `80`).

Assuming you mapped nginx's port 80 to `8880` on the host, your URLs would be:

- **Dashboard:**  
  `http://192.168.124.169:8880/dashboard/`

- **Web Portal:**  
  `http://192.168.124.169:8880/web/`

- **TensorBoard:**  
  `http://192.168.124.169:8880/tensorboard/`

- **Chroma:**  
  `http://192.168.124.169:8880/chroma/`

- **MLflow:**  
  `http://192.168.124.169:8880/mlflow/`

- **Label Studio:**  
  `http://192.168.124.169:8880/label-studio/`

- **Gitea:**  
  `http://192.168.124.169:8880/gitea/`

> If you mapped nginx to a different port (e.g., `80:80`), use that port instead of `8880`.

You can open these URLs in your browser from any device on the same network as your Raspberry Pi.
