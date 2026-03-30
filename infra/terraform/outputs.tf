output "name_prefix" {
  description = "Computed resource name prefix."
  value       = local.name_prefix
}

output "ecr_repository_url" {
  description = "ECR repository URL for PolicyGate image pushes."
  value       = aws_ecr_repository.policygate.repository_url
}

output "cloudwatch_log_group_name" {
  description = "CloudWatch log group for PolicyGate ECS logs."
  value       = aws_cloudwatch_log_group.policygate.name
}

output "alb_dns_name" {
  description = "Public DNS name of the PolicyGate ALB."
  value       = aws_lb.policygate.dns_name
}
