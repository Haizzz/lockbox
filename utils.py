# utility functions
import json
import datetime

import settings


class StatusManager():
    status_dict = {}

    def __init__(self):
        self.status_dict = json.load(open(settings.STATUS_FILE_PATH, "r"))

    def update(self, k, v, forced=False):
        """
        Update the status file with new details
        :param k: string key to update
        :param v: value to update with 
        :param forced: boolean whether or not to force the key update
        :return: None
        """
        # prevent salt and encrypted_check_phrase from being updated
        # unless forced
        if k in ["salt", "encrypted_check_phrase"] and not forced:
            raise KeyError("cannot update key {}".format(k))
        self.status_dict[k] = v
        json.dump(self.status_dict, open(settings.STATUS_FILE_PATH, "w"),
                  indent=4)

    def log_activity(self, msg):
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

    def get_status(self):
        """
        Open the status file and do any parsing required
        :return: dictionary
        """
        status = dict(self.status_dict)
        # salt and encrypted_check_phrase is stored as bytes.hex
        # reverse it with bytes.fromhex
        status["salt"] = bytes.fromhex(status["salt"])
        status["encrypted_check_phrase"] = bytes.fromhex(
            status["encrypted_check_phrase"])
        return status
