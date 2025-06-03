import os
import json
import urllib3
from datetime import datetime, timezone, timedelta

http = urllib3.PoolManager()

def format_bytes(size):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def get_australia_time():
    """Get current Australia time with DST handling"""
    now = datetime.now(timezone.utc)
    is_dst = now.month in [10, 11, 12, 1, 2, 3]  # Oct-Mar is DST
    return now + timedelta(hours=11 if is_dst else 10)

def lambda_handler(event, context):
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    slack_channel = os.environ["SLACK_CHANNEL"]
    environment = os.environ.get("ENVIRONMENT", "unknown")

    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    alarm_name = sns_message.get('AlarmName', 'UnknownAlarm')
    alarm_desc = sns_message.get('AlarmDescription', 'Database alert')
    new_state = sns_message.get('NewStateValue', 'UNKNOWN')
    trigger = sns_message.get("Trigger", {})

    metric_name = trigger.get("MetricName", "UnknownMetric")
    value = trigger.get("MetricValue")
    threshold = trigger.get("Threshold")

    # Extract DB identifier
    dimensions = trigger.get("Dimensions", [])
    db_identifier = "unknown"
    for d in dimensions:
        if d.get("name") in ["DBInstanceIdentifier", "DBClusterIdentifier"]:
            db_identifier = d.get("value")
            break

    aus_time = get_australia_time()

    # Emoji and color per metric type
    metric_meta = {
        "FreeableMemory": {"emoji": "🧠", "color": "#ff9900"},
        "FreeStorageSpace": {"emoji": "💾", "color": "#cc0000"},
        "CPUUtilization": {"emoji": "🖥️", "color": "#ff3300"},
        "Latency": {"emoji": "🐢", "color": "#9966ff"},
        "Deadlocks": {"emoji": "🔒", "color": "#ff0066"},
    }
    meta = metric_meta.get(metric_name, {"emoji": "⚠️", "color": "#cccccc"})
    emoji = meta["emoji"]
    color = meta["color"]

    # Format alert details
    if metric_name == "FreeableMemory" and value is not None and threshold is not None:
        formatted_value = format_bytes(value)
        formatted_threshold = format_bytes(threshold)
        title = f"{emoji} LOW MEMORY - {db_identifier}"
        details = f"""• Memory: {formatted_value}
• Threshold: {formatted_threshold}
• Database: {db_identifier}"""

    elif metric_name == "FreeStorageSpace" and value is not None and threshold is not None:
        formatted_value = format_bytes(value)
        formatted_threshold = format_bytes(threshold)
        title = f"{emoji} LOW STORAGE - {db_identifier}"
        details = f"""• Storage: {formatted_value}
• Threshold: {formatted_threshold}
• Database: {db_identifier}"""

    elif metric_name == "CPUUtilization" and value is not None and threshold is not None:
        title = f"{emoji} HIGH CPU - {db_identifier}"
        details = f"""• CPU: {value:.1f}%
• Threshold: {threshold}%
• Database: {db_identifier}"""

    elif metric_name == "Deadlocks" and value is not None and threshold is not None:
        title = f"{emoji} DEADLOCKS DETECTED - {db_identifier}"
        details = f"""• Deadlocks: {value:.1f}
• Threshold: {threshold}
• Database: {db_identifier}"""

    elif metric_name == "Latency" and value is not None and threshold is not None:
        title = f"{emoji} HIGH LATENCY - {db_identifier}"
        details = f"""• Latency: {value:.2f} ms
• Threshold: {threshold} ms
• Database: {db_identifier}"""

    else:
        title = f"{emoji} ALERT - {metric_name} - {db_identifier}"
        detail_lines = [f"• Database: {db_identifier}"]
        if value is not None:
            detail_lines.insert(0, f"• Value: {value}")
        if threshold is not None:
            detail_lines.insert(1, f"• Threshold: {threshold}")
        details = "\n".join(detail_lines)

    slack_msg = {
        "channel": slack_channel,
        "username": f"AWS {environment} Alert",
        "icon_emoji": ":warning:",
        "attachments": [{
            "color": color if new_state == "ALARM" else "#36A64F",
            "title": title,
            "text": alarm_desc,
            "fields": [
                {
                    "title": "Details",
                    "value": details,
                    "short": False
                },
                {
                    "title": "Environment",
                    "value": environment,
                    "short": True
                },
                {
                    "title": "Local Time",
                    "value": aus_time.strftime("%a, %d %b %Y %H:%M %Z"),
                    "short": True
                }
            ],
            "footer": "Investigate in CloudWatch → Alarms",
            "ts": int(aus_time.timestamp())
        }]
    }

    try:
        response = http.request(
            "POST",
            webhook_url,
            body=json.dumps(slack_msg),
            headers={"Content-Type": "application/json"}
        )
        if response.status != 200:
            print(f"Slack API error: {response.data.decode('utf-8')}")
    except Exception as e:
        print(f"Error sending to Slack: {str(e)}")
        raise

    return {"statusCode": 200}
