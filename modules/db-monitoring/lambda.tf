data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/lambda/slack_notifier.zip"
  source_dir  = "${path.module}/lambda"
  excludes    = ["slack_notifier.zip"] 
}

resource "aws_lambda_function" "slack_notifier" {
  filename      = data.archive_file.lambda_zip.output_path
  function_name = "${var.alarm_name_prefix}-slack-notifier"
  role          = aws_iam_role.lambda_execution.arn
  handler       = "slack_notifier.lambda_handler"
  runtime       = "python3.9"
  
  source_code_hash = filebase64sha256(data.archive_file.lambda_zip.output_path)
  
  environment {
    variables = {
      SLACK_WEBHOOK_URL = var.slack_webhook_url
      SLACK_CHANNEL     = var.slack_channel
      ENVIRONMENT       = var.environment
    }
  }
}

# resource "aws_lambda_function" "db_alerts" {
#   function_name = "${var.environment}-db-alerts"
#   role          = aws_iam_role.lambda_execution.arn
#   handler       = "index.lambda_handler"
#   runtime       = "python3.11"
#   filename      = "path/to/your/zip/file.zip"

#   environment {
#     variables = {
#       SLACK_WEBHOOK_URL = var.slack_webhook_url
#       SLACK_CHANNEL     = var.slack_channel
#       ENVIRONMENT       = var.environment  # <--- Set it explicitly
#     }
#   }

#   tags = var.tags
# }