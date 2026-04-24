output "ecr_repository_name" {
  value = aws_ecr_repository.this.name
}

output "ecr_repository_url" {
  value = aws_ecr_repository.this.repository_url
}

output "s3_bucket_name" {
  value = aws_s3_bucket.data.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.this.function_name
}

output "lambda_function_arn" {
  value = aws_lambda_function.this.arn
}

output "scheduler_name" {
  value = aws_scheduler_schedule.this.name
}