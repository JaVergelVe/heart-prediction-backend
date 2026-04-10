output "backend_public_ip" {
  description = "IP pública de la instancia EC2"
  value       = aws_eip.backend.public_ip
}

output "backend_url" {
  description = "URL base de la API"
  value       = "http://${aws_eip.backend.public_ip}:8000"
}

output "api_docs_url" {
  description = "Swagger UI"
  value       = "http://${aws_eip.backend.public_ip}:8000/docs"
}

output "health_check_url" {
  description = "Health check endpoint"
  value       = "http://${aws_eip.backend.public_ip}:8000/v1/health"
}

output "ssh_command" {
  description = "Comando SSH para conectarte a la instancia"
  value       = "ssh -i ~/.ssh/id_rsa ec2-user@${aws_eip.backend.public_ip}"
}

output "cloudwatch_log_group" {
  description = "Grupo de logs en CloudWatch"
  value       = aws_cloudwatch_log_group.backend_logs.name
}
