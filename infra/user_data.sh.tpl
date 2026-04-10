#!/bin/bash
set -euo pipefail
exec > >(tee /var/log/user-data.log | logger -t user-data) 2>&1

echo "=== [1/7] Actualizando sistema ==="
dnf update -y
dnf install -y docker git awscli

echo "=== [2/7] Iniciando Docker ==="
systemctl enable docker
systemctl start docker
usermod -aG docker ec2-user

echo "=== [3/7] Instalando Docker Compose ==="
curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64" \
  -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

echo "=== [4/7] Clonando repositorio ==="
mkdir -p /opt/heart-prediction
cd /opt/heart-prediction
git clone --branch ${git_branch} ${git_repo_url} backend
cd backend

echo "=== [5/7] Obteniendo secrets desde SSM Parameter Store ==="
AWS_REGION="${aws_region}"
PROJECT="${project_name}"

DB_URL=$(aws ssm get-parameter \
  --name "/$PROJECT/DATABASE_URL" \
  --with-decryption \
  --region "$AWS_REGION" \
  --query "Parameter.Value" \
  --output text)

JWT_SECRET=$(aws ssm get-parameter \
  --name "/$PROJECT/JWT_SECRET_KEY" \
  --with-decryption \
  --region "$AWS_REGION" \
  --query "Parameter.Value" \
  --output text)

echo "=== [6/7] Creando .env de producción ==="
cat > .env <<EOF
APP_NAME=Heart Attack Prediction API
DEBUG=false
API_VERSION=1.0.0
DATABASE_URL=$DB_URL
JWT_SECRET_KEY=$JWT_SECRET
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_SECONDS=86400
ML_MODELS_DIR=/app/app/ml/models
EOF

echo "=== [7/7] Levantando contenedor con Docker ==="
docker build -t heart-backend:latest .

docker run -d \
  --name heart_backend \
  --restart unless-stopped \
  -p 8000:8000 \
  --env-file .env \
  -v /opt/heart-prediction/backend/app/ml/models:/app/app/ml/models:ro \
  --log-driver=awslogs \
  --log-opt awslogs-region=${aws_region} \
  --log-opt awslogs-group=/heart-prediction/backend \
  --log-opt awslogs-stream=ec2-backend \
  --log-opt awslogs-create-group=true \
  heart-backend:latest

echo "=== Deploy completado ==="
echo "API disponible en: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8000"
