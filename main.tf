# module "db_monitoring" {
#   source = "./modules/db-monitoring"

#   db_identifier    = var.db_identifier
#   is_cluster       = var.is_cluster
#   environment      = var.environment
#   cpu_threshold    = var.cpu_threshold
#   memory_threshold = var.memory_threshold
#   slack_webhook_url = var.slack_webhook_url
#   slack_channel     = var.slack_channel
#   tags             = var.tags
# }


module "db_monitoring" {
  source = "./modules/db-monitoring"

  # Database Configuration
  db_identifiers = var.db_identifiers
  is_cluster     = var.is_cluster

  # Alert Thresholds
  cpu_threshold     = var.cpu_threshold
  memory_threshold  = var.memory_threshold
  latency_threshold = var.latency_threshold

  # Slack Configuration
  slack_webhook_url = var.slack_webhook_url
  slack_channel     = var.slack_channel
  
  # General
  alarm_name_prefix = var.alarm_name_prefix
  environment       = var.environment
  tags              = var.tags
}
