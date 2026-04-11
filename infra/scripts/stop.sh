#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# stop.sh — Detiene la instancia EC2 para no generar costos
#
# ⚠️  IMPORTANTE sobre costos al detener:
#   - EC2 detenida: NO cobra por cómputo ✅
#   - EBS (disco): SÍ cobra (~$0.10/GB/mes) — mínimo con 20GB = ~$2/mes
#   - Elastic IP sin instancia corriendo: SÍ cobra (~$0.005/hora) ⚠️
#
# Para costo CERO: usa destroy.sh en su lugar.
# Para pausar rápido y retomar: usa este script.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$SCRIPT_DIR/.."

cd "$INFRA_DIR"

INSTANCE_ID=$(terraform output -raw backend_public_ip 2>/dev/null | xargs -I{} aws ec2 describe-instances \
  --filters "Name=ip-address,Values={}" \
  --query "Reservations[0].Instances[0].InstanceId" \
  --output text 2>/dev/null || echo "")

if [ -z "$INSTANCE_ID" ] || [ "$INSTANCE_ID" = "None" ]; then
  # Alternativa: buscar por tag
  INSTANCE_ID=$(aws ec2 describe-instances \
    --filters "Name=tag:Project,Values=heart-prediction" "Name=instance-state-name,Values=running" \
    --query "Reservations[0].Instances[0].InstanceId" \
    --output text)
fi

if [ -z "$INSTANCE_ID" ] || [ "$INSTANCE_ID" = "None" ]; then
  echo "❌ No se encontró instancia EC2 corriendo."
  exit 1
fi

echo "🛑 Deteniendo instancia: $INSTANCE_ID"
aws ec2 stop-instances --instance-ids "$INSTANCE_ID"
aws ec2 wait instance-stopped --instance-ids "$INSTANCE_ID"

echo "✅ Instancia detenida."
echo ""
echo "⚠️  Recuerda: el EBS y la Elastic IP siguen generando costos mínimos."
echo "   Para costo CERO ejecuta: bash destroy.sh"
echo "   Para volver a levantar:  bash start.sh"
