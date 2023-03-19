from constance import config


rejection_message = f" but was **rejected**. You can check your access [here]({config.SITE_URL}/profile/access/view/)."
not_signed_in_message = " but was rejected because they aren't signed into site."

ok_color = 5025616
warning_color = 16750592
error_color = 16007990

door_messages = {
    "unlocked": {
        "text": ":unlock: {name} just **successfully** swiped at {door} door.",
        "color": ok_color,
    },
    "not_signed_in": {
        "text": ":lock: {name} swiped at {door} door" + not_signed_in_message,
        "color": ok_color,
    },
    "rejected": {
        "text": "{name} just swiped at {door} door" + rejection_message,
        "color": error_color,
    },
}

interlock_messages = {
    "activated": {
        "text": ":unlock: {name} just **activated** the {interlock}.",
        "color": ok_color,
    },
    "rejected": {
        "text": "{name} tried to activate the {interlock}" + rejection_message,
        "color": error_color,
    },
    "deactivated": {
        "text": ":lock: {name} just **deactivated** the {interlock}. It was on for {time}.",
        "color": ok_color,
    },
    "left_on": {
        "text": ":lock: The {interlock} was just turned off by the access system because it timed out (last used by {name}). It was on for {time}.",
        "color": warning_color,
    },
    "maintenance_lock_out": {
        "text": "{name} tried to access the {interlock} but it is currently under a maintenance lockout",
        "color": error_color,
    },
    "not_signed_in": {
        "text": ":lock: {name} swiped at {interlock}" + not_signed_in_message,
        "color": ok_color,
    },
}

kiosk_messages = {
    "signed_in": {
        "text": ":book: {name} just signed in at a kiosk.",
        "color": ok_color,
    },
    "signed_out": {
        "text": ":book: {name} just signed out at a kiosk.",
        "color": ok_color,
    },
}


def get_door_message(door, name, status):
    if status == True:
        message = door_messages["unlocked"]
    elif status in door_messages.keys():
        message = door_messages[status]
    else:
        message = door_messages["rejected"]

    return {
        "description": message["text"].format(name=name, door=door),
        "color": message["color"],
    }


def get_interlock_message(interlock, name, status, time):
    if status in interlock_messages.keys():
        message = interlock_messages[status]
    else:
        message = interlock_messages["rejected"]

    return {
        "description": message["text"].format(
            name=name, interlock=interlock, time=time
        ),
        "color": message["color"],
    }


def get_kiosk_message(name, sign_in):
    message = kiosk_messages["signed_in"] if sign_in else kiosk_messages["signed_out"]

    return {
        "description": message["text"].format(name=name),
        "color": message["color"],
    }
