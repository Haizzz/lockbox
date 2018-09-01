"""
Lockbox: quickly encrypt and decrypt an entire folder
"""
import json
import sys

import settings
from start import set_password, full_setup
from utils import StatusManager
from encryption import (
    encrypt_file,
    decrypt_file,
    recursive_file_action,
    generate_key_from_password,
    check_correct_password,
    check_folder_fully_decrypted
)
# check if this folder has been set up with a password before
if not os.path.isfile(settings.STATUS_FILE_PATH):
    # password not set, run initialisation function
    print("Lockbox has not been set up for this folder")
    print("Running setup process...")
    full_setup()
    print("Setup complete!")
else:
    status_manager = StatusManager()
    status = status_manager.get_status()
    # get action they want to take
    while True:
        print("Select an action: {}".format(
            ", ".join(settings.AVALAIBLE_ACTIONS)
        ))
        action_input = input("Action: ")
        if action_input.lower() in settings.AVALAIBLE_ACTIONS:
            break
        print("Invalid action given")
    if action_input == "reset":
        # folders have to be decrypted in order to reset password
        if not check_folder_fully_decrypted(settings.ENCRYPT_FOLDER_PATH):
            print("Folder must be fully decrypted before resetting password")
            sys.exit()
        full_setup()
        sys.exit()
    # whether encrypting or decrypting, still need the password input
    while True:
        password_input = input("Password: ")
        if check_correct_password(status, password_input):
            break
        print("Password entered is incorrect")

    key = generate_key_from_password(password_input, salt=status["salt"])
    if action_input == "encrypt":
        print("Encrypting files...")
        action = encrypt_file
        msg = "encrypted folder"
    elif action_input == "decrypt":
        print("Decrypting files...")
        action = decrypt_file
        msg = "encrypted folder"

    recursive_file_action(settings.ENCRYPT_FOLDER_PATH,
                          action, key)
    # log and set new encrypted status
    status_manager.log_activity(msg)
