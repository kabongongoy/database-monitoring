output "sns_topic_arn" {
  description = "ARN of the SNS topic for alarms"
  value       = aws_sns_topic.db_alarms.arn
}

output "lambda_function_arn" {
  description = "ARN of the Slack notifier Lambda"
  value       = aws_lambda_function.slack_notifier.arn
}