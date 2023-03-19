import requests
from constance import config
from django.conf import settings

from .notifier import Notifier


class DiscordNotifier(Notifier):
    def __init__(self):
        super().__init__(
            config.DISCORD_DOOR_WEBHOOK,
            config.DISCORD_INTERLOCK_WEBHOOK,
            config.DISCORD_DOOR_WEBHOOK,
        )

    def _is_enabled(self):
        return config.ENABLE_DISCORD_INTEGRATION

    @classmethod
    def _post_webhook(cls, url, message):
        json_message = {"description": "", "embeds": [message]}

        try:
            requests.post(url, json=json_message, timeout=settings.REQUEST_TIMEOUT)
        except requests.exceptions.ReadTimeout:
            return True
