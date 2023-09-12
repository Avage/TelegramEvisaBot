import re


def check_msg_validity(message):
    return bool(re.match("^[A-Za-z0-9. ]*$", message.text))
