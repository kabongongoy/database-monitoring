resource "aws_sns_topic" "db_alarms" {
  name = "${var.alarm_name_prefix}-alerts-${var.environment}"
  tags = var.tags
}

resource "aws_sns_topic_subscription" "lambda" {
  topic_arn = aws_sns_topic.db_alarms.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.slack_notifier.arn
}

# CPU Alarms for all databases
resource "aws_cloudwatch_metric_alarm" "cpu" {
  for_each            = toset(var.db_identifiers)
  alarm_name          = "${var.alarm_name_prefix}-cpu-${each.value}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 5
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = 60
  statistic           = "Average"
  threshold           = var.cpu_threshold
  alarm_description   = "Database CPU exceeds ${var.cpu_threshold}% for 5 minutes"
  alarm_actions       = [aws_sns_topic.db_alarms.arn]
  # ok_actions          = [aws_sns_topic.db_alarms.arn]
  
  dimensions = {
    DBInstanceIdentifier = var.is_cluster ? null : each.value
    DBClusterIdentifier  = var.is_cluster ? each.value : null
  }
  
  tags = merge(var.tags, {
    Metric   = "CPU"
    Database = each.value
  })
}

# Memory Alarms for all databases
resource "aws_cloudwatch_metric_alarm" "memory" {
  for_each            = toset(var.db_identifiers)
  alarm_name          = "${var.alarm_name_prefix}-memory-${each.value}"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 5
  metric_name         = "FreeableMemory"
  namespace           = "AWS/RDS"
  period              = 60
  statistic           = "Average"
  threshold           = var.memory_threshold
  alarm_description   = "Database memory below ${var.memory_threshold/1000000000}GB for 5 minutes"
  alarm_actions       = [aws_sns_topic.db_alarms.arn]
  # ok_actions          = [aws_sns_topic.db_alarms.arn]
  
  dimensions = {
    DBInstanceIdentifier = var.is_cluster ? null : each.value
    DBClusterIdentifier  = var.is_cluster ? each.value : null
  }
  
  tags = merge(var.tags, {
    Metric   = "Memory"
    Database = each.value
  })
}




# Latency Alarms for all databases
resource "aws_cloudwatch_metric_alarm" "latency" {
  for_each            = toset(var.db_identifiers)
  alarm_name          = "${var.alarm_name_prefix}-latency-${each.value}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 5
  metric_name         = "DatabaseConnections"
  namespace           = "AWS/RDS"
  period              = 60
  statistic           = "Average"
  threshold           = var.latency_threshold
  alarm_description   = "Database latency exceeds ${var.latency_threshold} seconds for 5 minutes"
  alarm_actions       = [aws_sns_topic.db_alarms.arn]
  # ok_actions          = [aws_sns_topic.db_alarms.arn]
  
  dimensions = {
    DBInstanceIdentifier = var.is_cluster ? null : each.value
    DBClusterIdentifier  = var.is_cluster ? each.value : null
  }
  
  tags = merge(var.tags, {
    Metric   = "Latency"
    Database = each.value
  })
}

resource "aws_cloudwatch_metric_alarm" "deadlocks" {
  for_each            = toset(var.db_identifiers)
  alarm_name          = "${var.alarm_name_prefix}-deadlocks-${each.value}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 5
  metric_name         = "Deadlocks"
  namespace           = "AWS/RDS"
  period              = 60
  statistic           = "Sum"
  threshold           = 1
  alarm_description   = "Database deadlocks detected for ${each.value} in the last 5 minutes"
  alarm_actions       = [aws_sns_topic.db_alarms.arn]
  # ok_actions          = [aws_sns_topic.db_alarms.arn]
  
  dimensions = {
    DBInstanceIdentifier = var.is_cluster ? null : each.value
    DBClusterIdentifier  = var.is_cluster ? each.value : null
  }
  
  tags = merge(var.tags, {
    Metric   = "Deadlocks"
    Database = each.value
  })
  
}
