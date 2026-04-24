locals {
  lambda_function_name = "${var.project_name}-lambda"
  schedule_name        = "${var.project_name}-schedule"

  ssm_username_parameter_arn = "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter${var.ssm_username_parameter_name}"
  ssm_password_parameter_arn = "arn:aws:ssm:${var.aws_region}:${data.aws_caller_identity.current.account_id}:parameter${var.ssm_password_parameter_name}"
}

# -------------------------
# ECR
# -------------------------

resource "aws_ecr_repository" "this" {
  name                 = var.ecr_repository_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = var.tags
}

# -------------------------
# S3
# -------------------------

resource "aws_s3_bucket" "data" {
  bucket = var.s3_bucket_name
  tags   = var.tags
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# -------------------------
# CloudWatch Logs
# -------------------------

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${local.lambda_function_name}"
  retention_in_days = var.log_retention_days
  tags              = var.tags
}

# -------------------------
# IAM - Lambda
# -------------------------

resource "aws_iam_role" "lambda_exec" {
  name = "${var.project_name}-lambda-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_app" {
  name = "${var.project_name}-lambda-app-policy"
  role = aws_iam_role.lambda_exec.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowS3IO"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = [
          "${aws_s3_bucket.data.arn}/${var.input_key}",
          "${aws_s3_bucket.data.arn}/${var.output_key}"
        ]
      },
      {
        Sid    = "AllowReadParameters"
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters"
        ]
        Resource = [
          local.ssm_username_parameter_arn,
          local.ssm_password_parameter_arn
        ]
      }
    ]
  })
}

# -------------------------
# Lambda
# -------------------------

resource "aws_lambda_function" "this" {
  function_name = local.lambda_function_name
  role          = aws_iam_role.lambda_exec.arn

  package_type = "Image"
  image_uri    = var.lambda_image_uri

  timeout     = var.lambda_timeout
  memory_size = var.lambda_memory_size

  ephemeral_storage {
    size = var.lambda_ephemeral_storage_mb
  }

  environment {
    variables = {
      ZP_S3_BUCKET         = aws_s3_bucket.data.bucket
      ZP_INPUT_KEY         = var.input_key
      ZP_OUTPUT_KEY        = var.output_key
      ZP_SSM_USERNAME_PARAM = var.ssm_username_parameter_name
      ZP_SSM_PASSWORD_PARAM = var.ssm_password_parameter_name
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.lambda
  ]

  tags = var.tags
}

# -------------------------
# IAM - Scheduler
# -------------------------

resource "aws_iam_role" "scheduler_invoke" {
  name = "${var.project_name}-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "scheduler.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = var.tags
}

resource "aws_iam_role_policy" "scheduler_invoke_lambda" {
  name = "${var.project_name}-scheduler-invoke-lambda"
  role = aws_iam_role.scheduler_invoke.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:InvokeFunction"
        ]
        Resource = aws_lambda_function.this.arn
      }
    ]
  })
}

# -------------------------
# EventBridge Scheduler
# -------------------------

resource "aws_scheduler_schedule" "this" {
  name                         = local.schedule_name
  schedule_expression          = var.schedule_expression
  schedule_expression_timezone = var.schedule_expression_timezone

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.this.arn
    role_arn = aws_iam_role.scheduler_invoke.arn

    input = jsonencode({
      source = "eventbridge-scheduler"
    })
  }
}