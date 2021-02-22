import json
import time
import logging

from updater.requests import send_request
from updater.settings import settings

LOG = logging.getLogger(__name__)


def send_notification(title, color, text, footer):
    channel = settings.SLACK_NOTIFICATION_CHANNEL
    url = settings.SLACK_HOOK
    icon = ':robot_face:'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    payload = {
        'channel': channel,
        'username': 'k8s-pod-updater',
        'icon_emoji': icon,
        'attachments': [
            {'fallback': title, 'color': color, 'title': title, 'text': text, 'footer': footer, 'ts': time.time()}
        ],
    }
    response = send_request(method='POST', url=url, payload=json.dumps(payload), headers=headers, auth="")
    LOG.info(f'Sent notification to Slack: {response.text}')
