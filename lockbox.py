"""
Lockbox: quickly encrypt and decrypt an entire folder
"""
import json

import settings
from start import setup
from utils import update_status, log_activity

status = json.load(open(settings.STATUS_FILE_PATH, "r"))
# check if this folder has been set up with a password before
if not status.get("password_set", False):
    # password not set, run initialisation function
    print("Lockbox has not been set up for this folder")
    print("Running setup process...")
    password_data = setup()
    # update status dict with new password details
    status["salt"] = password_data["salt"]
    status["hashed_password"] = password_data["hashed_password"]
    # set password_set to true
    status["password_set"] = True
    update_status(status)
    log_activity("set initial password")
    print("Setup successful!")
