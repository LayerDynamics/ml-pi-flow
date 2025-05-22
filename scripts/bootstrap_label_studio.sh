#!/usr/bin/env bash
# Bootstrap Label-Studio with a default project via its API.

set -euo pipefail
cd "$(dirname "$0")"/..

# load API key
if [ ! -f .env ]; then
  echo ".env file missing—copy .env.example and set LABEL_STUDIO_API_KEY"
  exit 1
fi
export $(grep -v '^#' .env | xargs)

API_URL="http://localhost:8080/api"
PROJECT_JSON=$(<scripts/default_label_project.json)

echo "Creating default Label-Studio project..."
curl -s -X POST "${API_URL}/projects" \
  -H "Authorization: Token ${LABEL_STUDIO_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "${PROJECT_JSON}" \
| jq .

echo "✅ Label-Studio project bootstrapped."
