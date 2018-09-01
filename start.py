# contain functions to setup lockbox in a new folder
import os
import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import settings
from encryption import generate_key_from_password
from utils import StatusManager


def set_password() -> dict:
    """
    Set a password for this folder,
    return the salt and encrypted check phrase in a dictionary
    :param:
    :return: dict
    """
    password = input("New password: ")
    print("Creating salt...")
    salt = os.urandom(16)
    print("Generating key...")
    key = generate_key_from_password(password, salt=salt)
    print("Generating check phrase...")
    # encrypt the check phrase so in the future the password
    # can be checked to see if it's correct
    f = Fernet(key)
    encrypted_check_phrase = f.encrypt(settings.CHECK_PHRASE)
    return {
        "salt": salt.hex(),
        "encrypted_check_phrase": encrypted_check_phrase.hex()
    }


def full_setup():
    """
    Do a full setup including creating necessary files. This will
    truncate any existing files
    Files:
    - logs
    - status.json
    """
    status_content = {
        "salt": "",
        "encrypted_check_phrase": ""
    }
    json.dump(status_content, open(settings.STATUS_FILE_PATH, "w+"),
              indent=4)
    status_manager = StatusManager()
    # do not truncate log file
    with open(settings.LOG_FILE_PATH, "a+") as f:
        pass
    # write log
    status_manager.log_activity("resetted data files")
    password_data = set_password()
    # update status dict with new password details
    status_manager.update("salt", password_data["salt"], forced=True)
    status_manager.update("encrypted_check_phrase",
                          password_data["encrypted_check_phrase"], forced=True)
    status_manager.log_activity("set new password")
