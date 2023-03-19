from constance import config

from .notifier import Notifier
from .discord_notifier import DiscordNotifier
from .slack_notifier import SlackNotifier


def get_notifier():
    if config.ENABLE_DISCORD_INTEGRATION:
        return DiscordNotifier()
    if config.ENABLE_SLACK_INTEGRATION:
        return SlackNotifier()
    else:
        return Notifier()
