#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# redeploy.sh — Actualiza el código en EC2 sin recrear la infraestructura
# Útil cuando haces cambios en el código y quieres actualizar sin terraform
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$SCRIPT_DIR/.."

cd "$INFRA_DIR"

EC2_IP=$(terraform output -raw backend_public_ip)
SSH_CMD="ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no ec2-user@$EC2_IP"

echo "🔄 Actualizando código en EC2: $EC2_IP"

$SSH_CMD << 'REMOTE'
  set -euo pipefail
  cd /opt/heart-prediction/backend

  echo "📥 Pulling últimos cambios..."
  git pull origin main

  echo "🏗️  Rebuilding imagen Docker..."
  docker build -t heart-backend:latest .

  echo "🔄 Reiniciando contenedor..."
  docker stop heart_backend || true
  docker rm heart_backend || true

  # Leer .env existente (ya tiene los secrets de SSM)
  docker run -d \
    --name heart_backend \
    --restart unless-stopped \
    -p 8000:8000 \
    --env-file .env \
    -v /opt/heart-prediction/backend/app/ml/models:/app/app/ml/models:ro \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=/heart-prediction/backend \
    --log-opt awslogs-stream=ec2-backend \
    heart-backend:latest

  echo "✅ Redeploy completado"
  docker ps | grep heart_backend
REMOTE

echo ""
echo "🌐 API: http://$EC2_IP:8000"
echo "📋 Health: curl http://$EC2_IP:8000/v1/health"
