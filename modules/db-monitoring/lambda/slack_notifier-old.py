# import os
# import json
# import urllib3
# from datetime import datetime
# from urllib.parse import quote

# http = urllib3.PoolManager()

# def lambda_handler(event, context):
#     # Configuration from environment variables
#     webhook_url = os.environ["SLACK_WEBHOOK_URL"]
#     slack_channel = os.environ["SLACK_CHANNEL"]
#     environment = os.environ.get("ENVIRONMENT", "unknown")
    
#     # Parse the CloudWatch alarm message
#     sns_message = json.loads(event["Records"][0]["Sns"]["Message"])
#     alarm_name = format_alarm_name(sns_message["AlarmName"])
#     alarm_description = sns_message.get("AlarmDescription", "Database monitoring alert")
#     new_state = sns_message["NewStateValue"]
#     reason = sns_message["NewStateReason"]
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M %Z")
    
#     # Create Jira investigation link (optional)
#     jira_link = create_jira_link(alarm_name, alarm_description, reason, environment)
    
#     # Format Slack message
#     slack_payload = format_slack_message(
#         alarm_name,
#         alarm_description,
#         new_state,
#         reason,
#         timestamp,
#         environment,
#         jira_link
#     )
    
#     # Send to Slack
#     send_slack_notification(webhook_url, slack_payload)

# def format_alarm_name(raw_name):
#     """Convert alarm names to human-readable format"""
#     return (raw_name
#             .replace("_", " ")
#             .replace("-", " ")
#             .title()
#             .replace("Cpu", "CPU")
#             .replace("Db", "DB")
#             .replace("Rds", "RDS"))

# def create_jira_link(alarm_name, description, reason, environment):
#     """Generate a Jira investigation link (optional)"""
#     jira_base_url = "https://your-jira-instance.atlassian.net/secure/CreateIssueDetails!init.jspa"
#     params = {
#         "pid": "12345",  # Your project ID
#         "issuetype": "1",  # Bug type
#         "summary": f"[AWS {environment}] {alarm_name}",
#         "description": f"*Description:* {description}\n\n*Reason:* {reason}",
#         "priority": "2",
#         "components": "cloudwatch-alerts"
#     }
#     query_string = "&".join(f"{k}={quote(v)}" for k,v in params.items())
#     return f"{jira_base_url}?{query_string}"

# def format_slack_message(name, description, state, reason, timestamp, env, jira_link):
#     """Create well-formatted Slack message with attachments"""
#     color, emoji = {
#         "ALARM": ("#FF0000", ":red_circle:"),
#         "OK": ("#36A64F", ":large_green_circle:"),
#         "INSUFFICIENT_DATA": ("#FFA500", ":warning:")
#     }.get(state, ("#764FA5", ":question:"))
    
#     return {
#         "channel": slack_channel,
#         "username": "AWS Database Monitor",
#         "icon_emoji": ":aws:",
#         "attachments": [
#             {
#                 "color": color,
#                 "title": f"{emoji} {name} - {state}",
#                 "text": f"*{description}*",
#                 "fields": [
#                     {"title": "Environment", "value": env, "short": True},
#                     {"title": "Status", "value": state, "short": True},
#                     {"title": "Timestamp", "value": timestamp, "short": True},
#                     {
#                         "title": "Details", 
#                         "value": f"```{reason}```\n\n<{jira_link}|Create Jira Ticket>",
#                         "short": False
#                     }
#                 ],
#                 "footer": "To investigate: Check CloudWatch -> RDS Metrics",
#                 "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
#                 "ts": datetime.now().timestamp()
#             }
#         ]
#     }

# def send_slack_notification(webhook_url, payload):
#     """Send message to Slack with error handling"""
#     try:
#         response = http.request(
#             "POST",
#             webhook_url,
#             body=json.dumps(payload),
#             headers={"Content-Type": "application/json"}
#         )
        
#         if response.status != 200:
#             raise Exception(f"Slack API error: {response.status} - {response.data.decode('utf-8')}")
            
#     except Exception as e:
#         print(f"Error sending to Slack: {str(e)}")
#         raise


# import os
# import json
# import urllib3
# from datetime import datetime
# from urllib.parse import quote

# http = urllib3.PoolManager()

# def lambda_handler(event, context):
#     # Configuration from environment variables
#     webhook_url = os.environ["SLACK_WEBHOOK_URL"]
#     slack_channel = os.environ["SLACK_CHANNEL"]
#     environment = os.environ.get("ENVIRONMENT", "unknown")
    
#     # Parse the CloudWatch alarm message
#     sns_message = json.loads(event["Records"][0]["Sns"]["Message"])
#     alarm_name = format_alarm_name(sns_message["AlarmName"])
#     alarm_description = sns_message.get("AlarmDescription", "Database monitoring alert")
#     new_state = sns_message["NewStateValue"]
#     reason = sns_message["NewStateReason"]
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M %Z")
    
#     # Create Jira investigation link (optional)
#     jira_link = create_jira_link(alarm_name, alarm_description, reason, environment)
    
#     # Format Slack message
#     slack_payload = format_slack_message(
#         alarm_name=alarm_name,
#         alarm_description=alarm_description,
#         state=new_state,
#         reason=reason,
#         timestamp=timestamp,
#         env=environment,
#         jira_link=jira_link,
#         slack_channel=slack_channel  # Added this parameter
#     )
    


#---------

# import os
# import json
# import urllib3
# from datetime import datetime

# http = urllib3.PoolManager()

# def lambda_handler(event, context):
#     # Get configuration from environment variables
#     webhook_url = os.environ["SLACK_WEBHOOK_URL"]
#     slack_channel = os.environ["SLACK_CHANNEL"]
    
#     # Parse the CloudWatch alarm
#     sns_message = json.loads(event["Records"][0]["Sns"]["Message"])
    
#     # Format message
#     message = {
#         "channel": slack_channel,  # Dynamic from Terraform
#         "username": "AWS Alarm",
#         "icon_emoji": ":aws:",
#         "attachments": [{
#             "color": "#FF0000" if sns_message["NewStateValue"] == "ALARM" else "#36A64F",
#             "title": f"{sns_message['AlarmName']} - {sns_message['NewStateValue']}",
#             "text": sns_message.get("AlarmDescription", "Database alert"),
#             "fields": [
#                 {"title": "Reason", "value": sns_message["NewStateReason"], "short": False},
#                 {"title": "Time", "value": datetime.now().strftime("%c"), "short": True}
#             ]
#         }]
#     }
    
#     # Send to Slack
#     http.request(
#         "POST",
#         webhook_url,
#         body=json.dumps(message),
#         headers={"Content-Type": "application/json"}
#     )
    
#     return {"statusCode": 200}
#     # Send to Slack
#     send_slack_notification(webhook_url, slack_payload)
#     return {"statusCode": 200}

# def format_alarm_name(raw_name):
#     """Convert alarm names to human-readable format"""
#     return (raw_name
#             .replace("_", " ")
#             .replace("-", " ")
#             .title()
#             .replace("Cpu", "CPU")
#             .replace("Db", "DB")
#             .replace("Rds", "RDS"))

# def create_jira_link(alarm_name, description, reason, environment):
#     """Generate a Jira investigation link (optional)"""
#     jira_base_url = "https://your-jira-instance.atlassian.net/secure/CreateIssueDetails!init.jspa"
#     params = {
#         "pid": "12345",  # Your project ID
#         "issuetype": "1",  # Bug type
#         "summary": f"[AWS {environment}] {alarm_name}",
#         "description": f"*Description:* {description}\n\n*Reason:* {reason}",
#         "priority": "2",
#         "components": "cloudwatch-alerts"
#     }
#     query_string = "&".join(f"{k}={quote(v)}" for k,v in params.items())
#     return f"{jira_base_url}?{query_string}"

# def format_slack_message(alarm_name, alarm_description, state, reason, timestamp, env, jira_link, slack_channel):
#     """Create well-formatted Slack message with attachments"""
#     color, emoji = {
#         "ALARM": ("#FF0000", ":red_circle:"),
#         "OK": ("#36A64F", ":large_green_circle:"),
#         "INSUFFICIENT_DATA": ("#FFA500", ":warning:")
#     }.get(state, ("#764FA5", ":question:"))
    
#     return {
#         "channel": slack_channel,
#         "username": "AWS Database Monitor",
#         "icon_emoji": ":aws:",
#         "attachments": [
#             {
#                 "color": color,
#                 "title": f"{emoji} {alarm_name} - {state}",
#                 "text": f"*{alarm_description}*",
#                 "fields": [
#                     {"title": "Environment", "value": env, "short": True},
#                     {"title": "Status", "value": state, "short": True},
#                     {"title": "Timestamp", "value": timestamp, "short": True},
#                     {
#                         "title": "Details", 
#                         "value": f"```{reason}```\n\n<{jira_link}|Create Jira Ticket>",
#                         "short": False
#                     }
#                 ],
#                 "footer": "To investigate: Check CloudWatch -> RDS Metrics",
#                 "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
#                 "ts": datetime.now().timestamp()
#             }
#         ]
#     }

# def send_slack_notification(webhook_url, payload):
#     """Send message to Slack with error handling"""
#     try:
#         response = http.request(
#             "POST",
#             webhook_url,
#             body=json.dumps(payload),
#             headers={"Content-Type": "application/json"}
#         )
        
#         if response.status != 200:
#             raise Exception(f"Slack API error: {response.status} - {response.data.decode('utf-8')}")
            
#     except Exception as e:
#         print(f"Error sending to Slack: {str(e)}")
#         raise







#---------

# import os
# import json
# import urllib3
# from datetime import datetime
# from pytz import timezone  # needs pytz package

# http = urllib3.PoolManager()

# def lambda_handler(event, context):
#     # Environment variables passed via Terraform
#     webhook_url = os.environ["SLACK_WEBHOOK_URL"]
#     slack_channel = os.environ["SLACK_CHANNEL"]
#     environment = os.environ.get("ENVIRONMENT", "unknown")

#     # Timezone: Australia/Sydney
#     au_tz = timezone("Australia/Sydney")
#     now_str = datetime.now(au_tz).strftime("%Y-%m-%d %H:%M:%S %Z")

#     # Parse SNS message from CloudWatch Alarm
#     sns_message = json.loads(event["Records"][0]["Sns"]["Message"])
#     alarm_name = format_alarm_name(sns_message["AlarmName"])
#     description = sns_message.get("AlarmDescription", "No description provided")
#     state = sns_message["NewStateValue"]
#     reason = sns_message["NewStateReason"]

#     # Prepare Slack payload
#     payload = format_slack_message(
#         alarm_name, description, state, reason, now_str, environment, slack_channel
#     )

#     # Send to Slack
#     send_slack_notification(webhook_url, payload)
#     return {"statusCode": 200}

# def format_alarm_name(raw_name):
#     return (raw_name
#             .replace("_", " ")
#             .replace("-", " ")
#             .title()
#             .replace("Cpu", "CPU")
#             .replace("Db", "DB")
#             .replace("Rds", "RDS"))

# def format_slack_message(name, desc, state, reason, timestamp, env, channel):
#     color, emoji = {
#         "ALARM": ("#FF0000", ":red_circle:"),
#         "OK": ("#36A64F", ":large_green_circle:"),
#         "INSUFFICIENT_DATA": ("#FFA500", ":warning:")
#     }.get(state, ("#764FA5", ":question:"))

#     return {
#         "channel": slack_channel,
#         "username": "AWS Monitor",
#         "icon_emoji": ":aws:",
#         "attachments": [{
#             "color": color,
#             "title": f"{emoji} {name} - {state}",
#             "text": f"*{desc}*",
#             "fields": [
#                 {"title": "Environment", "value": env, "short": True},
#                 {"title": "Status", "value": state, "short": True},
#                 {"title": "Timestamp", "value": timestamp, "short": True},
#                 {"title": "Details", "value": f"```{reason}```", "short": False}
#             ],
#             "footer": "CloudWatch → RDS Metrics",
#             "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
#             "ts": int(datetime.now().timestamp())
#         }]
#     }


# def send_slack_notification(webhook_url, payload):
#     try:
#         response = http.request(
#             "POST",
#             webhook_url,
#             body=json.dumps(payload),
#             headers={"Content-Type": "application/json"}
#         )
#         if response.status != 200:
#             raise Exception(f"Slack API error: {response.status} - {response.data.decode('utf-8')}")
#     except Exception as e:
#         print(f"Error sending to Slack: {e}")
#         raise
