# Lambda architecture v1

## Purpose
Initial AWS architecture sketch for the ZwiftPower Excel Updater project.

## Main components
- ECR – stores the container image for the Lambda function
- Lambda – runs the application logic
- EventBridge Scheduler – triggers the job on a schedule
- Parameter Store – stores `ZP_USERNAME` and `ZP_PASSWORD`
- S3 – stores the input and output files
- CloudWatch Logs – stores execution logs

## Runtime assumptions
- Lambda timeout: 840 s
- Soft stop in code: 800 s
- Temporary storage (`/tmp`): 2048 MB

## Input / Output
- input: `team.xlsx` in S3
- output: `updated_team.xlsx` in S3

## Notes
This is the first working version of the architecture for further Terraform work.