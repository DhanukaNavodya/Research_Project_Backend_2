#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-${EC2_APP_DIR:-/srv/research-backend}}"
VENV_DIR="${VENV_DIR:-.venv}"
MODEL_DIR="${MODEL_DIR:-app/ml/model/final_sinhala_mood_model}"
S3_BUCKET="${S3_BUCKET:-}"
S3_PREFIX="${S3_PREFIX:-}"
APP_SERVICE="${APP_SERVICE:-research-backend}"

cd "$APP_DIR"

git fetch origin main
if ! git rev-parse --verify main >/dev/null 2>&1; then
  git checkout -b main
else
  git checkout main
fi

git pull --ff-only origin main

if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"

pip install -r requirements.txt

if [ -n "$S3_BUCKET" ]; then
  mkdir -p "$MODEL_DIR"
  if [ -n "$S3_PREFIX" ]; then
    aws s3 sync "s3://$S3_BUCKET/$S3_PREFIX" "$MODEL_DIR" --only-show-errors
  else
    aws s3 sync "s3://$S3_BUCKET" "$MODEL_DIR" --only-show-errors
  fi
fi

sudo systemctl restart "$APP_SERVICE"
