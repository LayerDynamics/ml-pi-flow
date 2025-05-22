#!/usr/bin/env bash
# Daily backup of all service volumes

set -euo pipefail
TIMESTAMP=$(date +'%Y-%m-%d')
BACKUP_DIR=/home/ryan/ml_platform/backups
mkdir -p "$BACKUP_DIR"

ARCHIVE="${BACKUP_DIR}/backup-${TIMESTAMP}.tar.gz"
echo "Backing up volumes to ${ARCHIVE}..."

tar czf "$ARCHIVE" \
    -C /home/ryan/ml_platform mlflow/storage \
    -C /home/ryan/ml_platform tensorboard/logs \
    -C /home/ryan/ml_platform vector_db/data \
    -C /home/ryan/ml_platform label_studio/data \
    -C /home/ryan/ml_platform great_expectations/data_docs

# keep last 7 days
find "$BACKUP_DIR" -maxdepth 1 -type f -name 'backup-*.tar.gz' -mtime +7 -delete

echo "✅ Backup complete."
