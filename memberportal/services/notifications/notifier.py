from .messages import get_door_message, get_interlock_message, get_kiosk_message


class Notifier:
    def __init__(self, door_webhook=None, interlock_webhook=None, kiosk_webhook=None):
        self._door_webhook = door_webhook
        self._interlock_webhook = interlock_webhook
        self._kiosk_webhook = kiosk_webhook

    def notify_door_swipe(self, name, door, status):
        if self._is_enabled():
            self._post_webhook(self._door_webhook, get_door_message(door, name, status))

    def notify_interlock_swipe(self, name, interlock, status, time=None):
        if self._is_enabled():
            self._post_webhook(
                self._interlock_webhook,
                get_interlock_message(interlock, name, status, time),
            )

    def notify_kiosk_swipe(self, name, sign_in):
        if self._is_enabled():
            self._post_webhook(self._kiosk_webhook, get_kiosk_message(name, sign_in))

    def _is_enabled(self):
        return False

    @classmethod
    def _post_webhook(cls, url, message):
        pass
