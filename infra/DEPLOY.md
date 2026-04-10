# Guía de Despliegue — Heart Prediction Backend en AWS

## Arquitectura

```
Internet
    │
    ▼ puerto 8000
EC2 t2.micro (Amazon Linux 2023)
    │  Docker → FastAPI (uvicorn)
    │  IAM Role → SSM + CloudWatch
    │
    ▼ puerto 3306
RDS MySQL (ya existente)
    heart-attack-db.c8b06ios85re.us-east-1.rds.amazonaws.com

Secrets → AWS SSM Parameter Store (gratis)
Logs    → AWS CloudWatch Logs (gratis tier)
```

## Prerequisitos (instalar una sola vez)

### 1. Terraform
```bash
# Windows (con Chocolatey)
choco install terraform

# O descarga desde: https://developer.hashicorp.com/terraform/install
terraform --version  # debe ser >= 1.5
```

### 2. AWS CLI
```bash
# Windows
winget install Amazon.AWSCLI
# O: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html

aws configure
# AWS Access Key ID: [tu key]
# AWS Secret Access Key: [tu secret]
# Default region: us-east-1
# Default output format: json
```

### 3. Clave SSH
```bash
# Si no tienes una:
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa
```

---

## Despliegue desde cero

### Paso 1 — Configurar variables
```bash
cd heart-prediction-backend/infra
cp terraform.tfvars.example terraform.tfvars
# Edita terraform.tfvars con tus valores reales
```

Variables críticas a editar:
- `database_url` → tu URL de RDS (ya la tienes en .env)
- `jwt_secret_key` → genera con: `python -c "import secrets; print(secrets.token_hex(32))"`
- `git_repo_url` → URL de tu repositorio
- `ssh_allowed_cidr` → tu IP: `curl ifconfig.me/ip` → `"203.x.x.x/32"`

### Paso 2 — Configurar RDS para aceptar conexiones de EC2
En AWS Console → RDS → tu instancia → Security Groups:
- Agrega regla Inbound: MySQL/Aurora, puerto 3306, Source: `0.0.0.0/0` (temporal)
- Después del deploy, restringe al SG de EC2 (más seguro)

### Paso 3 — Desplegar
```bash
bash scripts/deploy.sh
```

Esto crea:
- EC2 t2.micro con Docker
- Elastic IP fija
- IAM Role con permisos SSM + CloudWatch
- SSM Parameters con tus secrets
- CloudWatch Log Group

### Paso 4 — Verificar
```bash
# Espera ~5 minutos para que EC2 arranque Docker
curl $(terraform output -raw health_check_url)

# Ver logs de arranque
ssh -i ~/.ssh/id_rsa ec2-user@$(terraform output -raw backend_public_ip) \
  'sudo tail -100 /var/log/user-data.log'

# Ver logs de la API en tiempo real
ssh -i ~/.ssh/id_rsa ec2-user@$(terraform output -raw backend_public_ip) \
  'docker logs -f heart_backend'
```

---

## Gestión de costos

### Detener (pausa rápida — costo mínimo)
```bash
bash scripts/stop.sh
```
- EC2 detenida: $0 cómputo
- EBS 20GB: ~$2/mes
- Elastic IP sin instancia: ~$3.60/mes ⚠️

### Volver a levantar
```bash
bash scripts/start.sh
```

### Destruir todo (costo = $0)
```bash
bash scripts/destroy.sh
```
La RDS NO se elimina.

### Volver a desplegar desde cero
```bash
bash scripts/deploy.sh
```

---

## Actualizar código sin recrear infraestructura
```bash
# Después de hacer git push de tus cambios:
bash scripts/redeploy.sh
```

---

## Ver logs en CloudWatch
```bash
# Últimas 50 líneas
aws logs get-log-events \
  --log-group-name /heart-prediction/backend \
  --log-stream-name ec2-backend \
  --limit 50 \
  --query "events[*].message" \
  --output text
```

O en AWS Console → CloudWatch → Log Groups → `/heart-prediction/backend`

---

## Estimación de costos (Free Tier)

| Recurso | Free Tier | Costo fuera |
|---------|-----------|-------------|
| EC2 t2.micro | 750h/mes (1er año) | ~$8.50/mes |
| EBS 20GB | 30GB/mes | ~$2/mes |
| RDS t3.micro | 750h/mes (1er año) | ~$15/mes |
| SSM Parameter Store | Gratis (Standard) | $0 |
| CloudWatch Logs | 5GB/mes gratis | $0.50/GB extra |
| Elastic IP (corriendo) | Gratis | $0 |
| Elastic IP (detenida) | ⚠️ $0.005/hora | ~$3.60/mes |

**Recomendación**: Destruye la infraestructura cuando no la uses. El redeploy tarda ~5 minutos.

---

## Troubleshooting

### La API no responde después del deploy
```bash
# Ver logs de user-data (arranque de EC2)
ssh -i ~/.ssh/id_rsa ec2-user@IP 'sudo cat /var/log/user-data.log'

# Ver estado del contenedor
ssh -i ~/.ssh/id_rsa ec2-user@IP 'docker ps -a'

# Ver logs del contenedor
ssh -i ~/.ssh/id_rsa ec2-user@IP 'docker logs heart_backend'
```

### Error de conexión a RDS
- Verifica que el SG de RDS permite tráfico desde la IP de EC2 en puerto 3306
- Verifica la DATABASE_URL en SSM: `aws ssm get-parameter --name /heart-prediction/DATABASE_URL --with-decryption`

### Modelos ML no encontrados
- Los modelos deben estar en `app/ml/models/` en el repositorio
- Verifica que el volumen Docker está montado correctamente
