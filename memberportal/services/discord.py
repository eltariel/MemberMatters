from .notifications import get_notifier


def post_door_swipe_to_discord(name, door, status):
    get_notifier().notify_door_swipe(name, door, status)
    return True


def post_interlock_swipe_to_discord(name, interlock, status, time=None):
    get_notifier().notify_interlock_swipe(name, interlock, status, time)
    return True


def post_kiosk_swipe_to_discord(name, sign_in):
    get_notifier().notify_kiosk_swipe(name, sign_in)
    return True
