#!/usr/bin/env bash
# Generate Great Expectations data docs from existing expectations.

set -euo pipefail
cd "$(dirname "$0")"/..

echo "Running Great Expectations docs build inside container..."
# assumes container is named `great_expectations` per docker-compose.yml
docker exec -u root great_expectations \
  great_expectations docs build

echo "✅ Great Expectations data docs generated."
