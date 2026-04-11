#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# deploy.sh — Despliega el backend desde cero en AWS
# Uso: bash deploy.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$SCRIPT_DIR/.."

echo "╔══════════════════════════════════════════════╗"
echo "║   Heart Prediction — Deploy a AWS            ║"
echo "╚══════════════════════════════════════════════╝"

# ── Verificar prerequisitos ──────────────────────────────────────────────────
command -v terraform >/dev/null 2>&1 || { echo "❌ Terraform no instalado. Ver: https://developer.hashicorp.com/terraform/install"; exit 1; }
command -v aws >/dev/null 2>&1       || { echo "❌ AWS CLI no instalado. Ver: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html"; exit 1; }

echo "✅ Prerequisitos OK"

# ── Verificar credenciales AWS ───────────────────────────────────────────────
echo "🔑 Verificando credenciales AWS..."
aws sts get-caller-identity --query "Account" --output text || {
  echo "❌ Credenciales AWS no configuradas. Ejecuta: aws configure"
  exit 1
}

# ── Verificar terraform.tfvars ───────────────────────────────────────────────
cd "$INFRA_DIR"
if [ ! -f "terraform.tfvars" ]; then
  echo "❌ No existe terraform.tfvars"
  echo "   Copia el ejemplo: cp terraform.tfvars.example terraform.tfvars"
  echo "   Luego edita los valores y vuelve a ejecutar."
  exit 1
fi

# ── Verificar clave SSH ──────────────────────────────────────────────────────
SSH_KEY_PATH=$(grep ssh_public_key_path terraform.tfvars | cut -d'"' -f2 | sed 's|~|'"$HOME"'|')
if [ ! -f "$SSH_KEY_PATH" ]; then
  echo "⚠️  No se encontró clave SSH en: $SSH_KEY_PATH"
  echo "   Genera una con: ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa"
  exit 1
fi

# ── Terraform ────────────────────────────────────────────────────────────────
echo ""
echo "🏗️  Inicializando Terraform..."
terraform init

echo ""
echo "📋 Plan de cambios:"
terraform plan -out=tfplan

echo ""
read -p "¿Aplicar los cambios? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
  echo "Cancelado."
  exit 0
fi

echo ""
echo "🚀 Aplicando infraestructura..."
terraform apply tfplan

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   ✅ Deploy completado                       ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "📌 Outputs:"
terraform output

echo ""
echo "⏳ La instancia EC2 tarda ~3-5 minutos en iniciar Docker y la API."
echo "   Verifica el estado con:"
echo "   curl \$(terraform output -raw health_check_url)"
echo ""
echo "📋 Ver logs de arranque:"
echo "   ssh -i ~/.ssh/id_rsa ec2-user@\$(terraform output -raw backend_public_ip) 'sudo tail -f /var/log/user-data.log'"
