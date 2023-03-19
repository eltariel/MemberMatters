import requests
import re

from constance import config
from django.conf import settings

from .notifier import Notifier


class SlackNotifier(Notifier):
    def __init__(self):
        super().__init__(
            config.SLACK_DOOR_WEBHOOK,
            config.SLACK_INTERLOCK_WEBHOOK,
            config.SLACK_DOOR_WEBHOOK,
        )

    def _is_enabled(self):
        return config.ENABLE_SLACK_INTEGRATION

    def _post_webhook(self, url, message):
        json_message = _slack_message(message["description"], message["color"])

        try:
            requests.post(url, json=json_message, timeout=settings.REQUEST_TIMEOUT)
        except requests.exceptions.ReadTimeout:
            return True


def _slack_message(markdown, color):
    """
    Create a Slack webhook payload that describes a (legacy) message with a colored band.
    """
    text = _markdown_to_slack(markdown)
    return {
        "attachments": [
            {
                "text": text,
                "fallback": text,
                "mrkdwn_in": ["text", "fallback"],
                "color": f"#{color:06X}",
            }
        ]
    }


def _markdown_to_slack(text):
    """
    Convert proper Markdown to Slack-style "mrkdwn" formatting. See https://api.slack.com/reference/surfaces/formatting
    for more details on this format.

    Currently implements the subset needed to render the existing door messages:
    - Bold: ** -> *
    - Links: [text](url) -> <url|text>
    """
    return re.sub(r"\[([^]]*)]\(([^)]*)\)", r"<\2|\1>", text.replace("**", "*"))
