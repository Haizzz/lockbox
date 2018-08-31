# utility functions
import json
import datetime

import settings


def update_status(new_status):
    """
    Update the status file with new details
    :param new_status: dict new status dictionary to write to file
    :return: None
    """
    json.dump(new_status, open(settings.STATUS_FILE_PATH, "w"),
              indent=4)


def log_activity(msg):
    """
    Add an entry to the activity log. Logs are in the format
    DATETIME_NOW > msg
    :param status: dict current status dictionary
    :param msg: the message for the log
    :return: None
    """
    now = datetime.datetime.utcnow()
    log_message = "{} > {}\n".format(now.isoformat(), msg)
    with open(settings.LOG_FILE_PATH, "a") as f:
        f.write(log_message)
