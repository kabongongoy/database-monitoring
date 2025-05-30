
output "alarm_sns_topic_arn" {
  description = "ARN of the SNS topic for alarm notifications"
  value       = module.db_monitoring.sns_topic_arn
}
