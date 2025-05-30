# output "alarm_sns_topic_arn" {
#   description = "ARN of the SNS topic for alarm notifications"
#   value       = aws_sns_topic.db_alarms.arn
# }

# output "alarm_names" {
#   description = "Names of all created CloudWatch alarms"
#   value       = module.db_alarms.all_alarm_names
# }

output "alarm_sns_topic_arn" {
  description = "ARN of the SNS topic for alarm notifications"
  value       = module.db_monitoring.sns_topic_arn
}
