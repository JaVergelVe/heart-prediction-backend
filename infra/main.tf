terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ─────────────────────────────────────────────
# DATA: VPC y subredes por defecto (sin costo)
# ─────────────────────────────────────────────
data "aws_vpc" "default" {
  default = true
}

# ─────────────────────────────────────────────
# DATA: Amazon Linux 2023 AMI más reciente
# ─────────────────────────────────────────────
data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# ─────────────────────────────────────────────
# SSM Parameter Store — secrets (GRATIS)
# ─────────────────────────────────────────────
resource "aws_ssm_parameter" "database_url" {
  name  = "/${var.project_name}/DATABASE_URL"
  type  = "SecureString"
  value = var.database_url
  tags  = local.common_tags
}

resource "aws_ssm_parameter" "jwt_secret" {
  name  = "/${var.project_name}/JWT_SECRET_KEY"
  type  = "SecureString"
  value = var.jwt_secret_key
  tags  = local.common_tags
}

# ─────────────────────────────────────────────
# Security Group para EC2
# ─────────────────────────────────────────────
resource "aws_security_group" "backend_sg" {
  name        = "${var.project_name}-backend-sg"
  description = "Heart Prediction Backend SG"
  vpc_id      = data.aws_vpc.default.id

  # HTTP API
  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "FastAPI"
  }

  # SSH (restringe a tu IP en producción)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
    description = "SSH admin"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = local.common_tags
}

# ─────────────────────────────────────────────
# IAM Role para EC2 → SSM + CloudWatch
# ─────────────────────────────────────────────
resource "aws_iam_role" "ec2_role" {
  name = "${var.project_name}-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
    }]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy" "ec2_ssm_policy" {
  name = "${var.project_name}-ssm-policy"
  role = aws_iam_role.ec2_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath"
        ]
        Resource = "arn:aws:ssm:${var.aws_region}:*:parameter/${var.project_name}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:*:log-group:/heart-prediction/*"
      },
      {
        # Para descifrar SecureString con KMS default
        Effect   = "Allow"
        Action   = ["kms:Decrypt"]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          "arn:aws:s3:::heart-prediction-ml-models",
          "arn:aws:s3:::heart-prediction-ml-models/*"
        ]
      }
    ]
  })
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.project_name}-ec2-profile"
  role = aws_iam_role.ec2_role.name
}

# ─────────────────────────────────────────────
# CloudWatch Log Group
# ─────────────────────────────────────────────
resource "aws_cloudwatch_log_group" "backend_logs" {
  name              = "/heart-prediction/backend"
  retention_in_days = 7   # Mínimo para no acumular costos
  tags              = local.common_tags
}

# ─────────────────────────────────────────────
# Key Pair SSH
# ─────────────────────────────────────────────
resource "aws_key_pair" "deployer" {
  key_name   = "${var.project_name}-key"
  public_key = file(var.ssh_public_key_path)
  tags       = local.common_tags
}

# ─────────────────────────────────────────────
# EC2 t2.micro — Free Tier
# ─────────────────────────────────────────────
resource "aws_instance" "backend" {
  ami                    = data.aws_ami.al2023.id   # Amazon Linux 2023 (resuelto dinámicamente)
  instance_type          = "t2.micro"
  key_name               = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.backend_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  subnet_id              = tolist(data.aws_subnets.default.ids)[0]

  # IP pública (sin NAT Gateway = sin costo)
  associate_public_ip_address = true

  root_block_device {
    volume_size = 30    # GB — Free Tier incluye 30GB EBS (AL2023 requiere >= 30GB)
    volume_type = "gp2"
  }

  user_data = templatefile("${path.module}/user_data.sh.tpl", {
    project_name = var.project_name
    aws_region   = var.aws_region
    git_repo_url = var.git_repo_url
    git_branch   = var.git_branch
  })

  tags = merge(local.common_tags, {
    Name = "${var.project_name}-backend"
  })
}

# ─────────────────────────────────────────────
# Elastic IP (gratis mientras la instancia corre)
# ⚠️ ADVERTENCIA: Si la instancia está DETENIDA y
# tienes EIP asociada, AWS cobra ~$0.005/hora.
# Destruye con: terraform destroy -target=aws_eip.backend
# ─────────────────────────────────────────────
resource "aws_eip" "backend" {
  instance = aws_instance.backend.id
  domain   = "vpc"
  tags     = local.common_tags
}

locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
