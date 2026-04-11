variable "aws_region" {
  description = "Región AWS donde desplegar"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nombre del proyecto (usado como prefijo en recursos)"
  type        = string
  default     = "heart-prediction"
}

variable "environment" {
  description = "Entorno (dev, staging, prod)"
  type        = string
  default     = "dev"
}

# ─── SSH ───────────────────────────────────────
variable "ssh_public_key_path" {
  description = "Ruta al archivo de clave pública SSH (~/.ssh/id_rsa.pub)"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "ssh_allowed_cidr" {
  description = "CIDR IP permitida para SSH. Usa tu IP: curl ifconfig.me/ip"
  type        = string
  default     = "0.0.0.0/0"  # ⚠️ Cambia a tu IP real: "203.0.113.10/32"
}

# ─── Secrets (se guardan en SSM) ───────────────
variable "database_url" {
  description = "URL de conexión MySQL a RDS"
  type        = string
  sensitive   = true
  # Ejemplo: mysql+pymysql://root:Root1234@heart-attack-db.c8b06ios85re.us-east-1.rds.amazonaws.com:3306/heart_attack_prediction
}

variable "jwt_secret_key" {
  description = "Secret key para firmar JWT"
  type        = string
  sensitive   = true
}

# ─── Git ───────────────────────────────────────
variable "git_repo_url" {
  description = "URL del repositorio Git del backend"
  type        = string
  default     = "https://github.com/JaVergelVe/heart-prediction-backend.git"
}

variable "git_branch" {
  description = "Rama a desplegar"
  type        = string
  default     = "develop"
}
