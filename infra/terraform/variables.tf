variable "aws_region" {
  description = "AWS region for PolicyGate infrastructure."
  type        = string
}

variable "project_name" {
  description = "Project name prefix for AWS resources."
  type        = string
  default     = "policygate"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
}
