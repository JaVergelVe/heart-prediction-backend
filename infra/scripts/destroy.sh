#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# destroy.sh — Destruye TODA la infraestructura (costo = $0)
# ⚠️  Esto elimina EC2, EIP, SGs, IAM roles, SSM params, CloudWatch logs.
#     La RDS NO se toca (es un recurso externo a este Terraform).
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$SCRIPT_DIR/.."

cd "$INFRA_DIR"

echo "╔══════════════════════════════════════════════╗"
echo "║   ⚠️  DESTRUIR INFRAESTRUCTURA               ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "Esto eliminará:"
echo "  - Instancia EC2"
echo "  - Elastic IP"
echo "  - Security Groups"
echo "  - IAM Role / Instance Profile"
echo "  - SSM Parameters (secrets)"
echo "  - CloudWatch Log Group"
echo ""
echo "NO se elimina: RDS MySQL (gestionado externamente)"
echo ""
read -p "¿Confirmas la destrucción? Escribe 'destroy' para continuar: " CONFIRM

if [ "$CONFIRM" != "destroy" ]; then
  echo "Cancelado."
  exit 0
fi

echo ""
echo "🗑️  Destruyendo infraestructura..."
terraform destroy -auto-approve

echo ""
echo "✅ Infraestructura destruida. Costo = \$0."
echo "   Para volver a desplegar: bash deploy.sh"
