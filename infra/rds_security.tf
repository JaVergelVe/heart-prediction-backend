# ─────────────────────────────────────────────────────────────────────────────
# Permite que el Security Group de EC2 acceda al puerto 3306 de RDS
#
# INSTRUCCIONES:
# 1. Ve a AWS Console → RDS → tu instancia → Security Groups
# 2. Edita el SG de RDS y agrega una regla Inbound:
#    - Type: MySQL/Aurora
#    - Port: 3306
#    - Source: el Security Group ID de EC2 (output de `terraform output`)
#
# O usa este recurso si conoces el SG ID de tu RDS:
# ─────────────────────────────────────────────────────────────────────────────

# Descomenta y completa si quieres que Terraform gestione la regla de RDS:

# data "aws_security_group" "rds_sg" {
#   id = "sg-XXXXXXXX"  # SG ID de tu RDS existente
# }
#
# resource "aws_security_group_rule" "rds_allow_ec2" {
#   type                     = "ingress"
#   from_port                = 3306
#   to_port                  = 3306
#   protocol                 = "tcp"
#   source_security_group_id = aws_security_group.backend_sg.id
#   security_group_id        = data.aws_security_group.rds_sg.id
#   description              = "Allow EC2 backend to connect to RDS MySQL"
# }

# ─────────────────────────────────────────────────────────────────────────────
# ALTERNATIVA RÁPIDA (menos segura, solo para tesis):
# En el SG de RDS, permite 0.0.0.0/0 en puerto 3306 temporalmente.
# Recuerda restringirlo después.
# ─────────────────────────────────────────────────────────────────────────────
