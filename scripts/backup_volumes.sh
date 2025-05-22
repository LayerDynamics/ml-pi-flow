#!/usr/bin/env bash
# Daily backup of all service volumes

set -euo pipefail
TIMESTAMP=$(date +'%Y-%m-%d')
BACKUP_DIR=/home/pi/ml-pi-flow/backups
mkdir -p "$BACKUP_DIR"

ARCHIVE="${BACKUP_DIR}/backup-${TIMESTAMP}.tar.gz"
echo "Backing up volumes to ${ARCHIVE}..."

tar czf "$ARCHIVE" \
    -C /home/pi/ml-pi-flow mlflow/storage \
    -C /home/pi/ml-pi-flow tensorboard/logs \
    -C /home/pi/ml-pi-flow vector_db/data \
    -C /home/pi/ml-pi-flow label_studio/data \
    -C /home/pi/ml-pi-flow great_expectations/data_docs

# keep last 7 days
find "$BACKUP_DIR" -maxdepth 1 -type f -name 'backup-*.tar.gz' -mtime +7 -delete

echo "✅ Backup complete."
