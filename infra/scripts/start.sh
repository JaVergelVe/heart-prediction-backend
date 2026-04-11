#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# start.sh — Vuelve a levantar la instancia EC2 detenida
# El contenedor Docker arranca automáticamente (restart: unless-stopped)
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$SCRIPT_DIR/.."

cd "$INFRA_DIR"

INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Project,Values=heart-prediction" "Name=instance-state-name,Values=stopped" \
  --query "Reservations[0].Instances[0].InstanceId" \
  --output text)

if [ -z "$INSTANCE_ID" ] || [ "$INSTANCE_ID" = "None" ]; then
  echo "❌ No se encontró instancia EC2 detenida con tag Project=heart-prediction"
  echo "   Si no existe, despliega desde cero con: bash deploy.sh"
  exit 1
fi

echo "▶️  Iniciando instancia: $INSTANCE_ID"
aws ec2 start-instances --instance-ids "$INSTANCE_ID"
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"

echo "✅ Instancia corriendo."
echo ""
echo "📌 Outputs actualizados:"
terraform output

echo ""
echo "⏳ El contenedor Docker arranca automáticamente en ~30 segundos."
echo "   Verifica con: curl \$(terraform output -raw health_check_url)"
