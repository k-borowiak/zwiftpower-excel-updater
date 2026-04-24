variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "project_name" {
  description = "Project name used as a prefix for resources"
  type        = string
  default     = "zwiftpower-updater"
}

variable "ecr_repository_name" {
  description = "ECR repository name"
  type        = string
  default     = "zwiftpower-updater"
}

variable "lambda_image_uri" {
  description = "Full ECR image URI for the Lambda function"
  type        = string
}

variable "s3_bucket_name" {
  description = "S3 bucket for input/output files"
  type        = string
}

variable "input_key" {
  description = "S3 key for input file"
  type        = string
  default     = "input/team.xlsx"
}

variable "output_key" {
  description = "S3 key for output file"
  type        = string
  default     = "output/updated_team.xlsx"
}

variable "ssm_username_parameter_name" {
  description = "SSM parameter name for ZwiftPower username"
  type        = string
}

variable "ssm_password_parameter_name" {
  description = "SSM parameter name for ZwiftPower password"
  type        = string
}

variable "schedule_expression" {
  description = "EventBridge Scheduler expression"
  type        = string
  default     = "rate(1 day)"
}

variable "schedule_expression_timezone" {
  description = "Timezone for the schedule expression"
  type        = string
  default     = "UTC"
}

variable "lambda_timeout" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 840
}

variable "lambda_memory_size" {
  description = "Lambda memory size in MB"
  type        = number
  default     = 1024
}

variable "lambda_ephemeral_storage_mb" {
  description = "Lambda /tmp storage size in MB"
  type        = number
  default     = 2048
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 14
}

variable "tags" {
  description = "Common tags"
  type        = map(string)
  default     = {}
}