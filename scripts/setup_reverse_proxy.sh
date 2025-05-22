#!/usr/bin/env bash
#
# Deploy Nginx reverse‐proxy config and obtain a Let's Encrypt cert.

set -euo pipefail

NGINX_CONF_PATH="/etc/nginx/sites-available/ml_platform.conf"
CERTBOT_EMAIL="${CERTBOT_EMAIL:-}"

if [[ $EUID -ne 0 ]]; then
  echo "⚠️  Please run as root or via sudo."
  exit 1
fi

if [[ -z "$CERTBOT_EMAIL" ]]; then
  echo "❌ CERTBOT_EMAIL not set. Please export CERTBOT_EMAIL in your environment or .env."
  exit 1
fi

echo "📄 Writing Nginx proxy config to $NGINX_CONF_PATH..."
cat > "$NGINX_CONF_PATH" <<'EOF'
upstream web_portal  { server localhost:9090; }
upstream dashboard   { server localhost:9000; }
upstream mlflow      { server localhost:5000; }
upstream tensorboard { server localhost:6006; }
upstream vector_db   { server localhost:8000; }
upstream label_studio{ server localhost:8080; }
upstream ge          { server localhost:5050; }

server {
    listen 80;
    server_name mlplatform.local;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mlplatform.local;

    ssl_certificate     /etc/letsencrypt/live/mlplatform.local/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mlplatform.local/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://web_portal;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    location /dashboard/ {
        rewrite ^/dashboard/(.*)$ /$1 break;
        proxy_pass http://dashboard;
        proxy_set_header Host $host;
    }
    location /mlflow/ {
        rewrite ^/mlflow/(.*)$ /$1 break;
        proxy_pass http://mlflow;
    }
    location /tensorboard/ {
        rewrite ^/tensorboard/(.*)$ /$1 break;
        proxy_pass http://tensorboard;
    }
    location /vector_db/ {
        rewrite ^/vector_db/(.*)$ /$1 break;
        proxy_pass http://vector_db;
    }
    location /label_studio/ {
        rewrite ^/label_studio/(.*)$ /$1 break;
        proxy_pass http://label_studio;
    }
    location /ge/ {
        rewrite ^/ge/(.*)$ /$1 break;
        proxy_pass http://ge;
    }
}
EOF

echo "🔗 Enabling site..."
ln -sf "$NGINX_CONF_PATH" /etc/nginx/sites-enabled/

echo "🔄 Testing Nginx configuration..."
nginx -t

echo "🚦 Restarting Nginx..."
systemctl restart nginx

echo "🔒 Obtaining SSL certificate via Certbot..."
certbot --nginx \
  --non-interactive \
  --agree-tos \
  --redirect \
  --email "$CERTBOT_EMAIL" \
  -d mlplatform.local

echo "🎉 Nginx reverse proxy set up with SSL."
