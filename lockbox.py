"""
Lockbox: quickly encrypt and decrypt an entire folder
"""
import json

import settings
from start import set_password, full_setup
from utils import StatusManager
from encryption import (
    encrypt_file,
    decrypt_file,
    recursive_file_action,
    generate_key_from_password,
    check_correct_password
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
    # whether encrypting or decrypting, still need the password input
    input_password = input("Password, // to reset password: ")
    if input_password == "//":
        # folders have to be decrypted in order to reset password
        if status["encrypted"]:
            print("Folder must be decrypted before resetting password")
            exit()
        full_setup()
        exit()
    if not check_correct_password(status, input_password):
        print("Password entered is incorrect")
        exit()
    else:
        key = generate_key_from_password(input_password, salt=status["salt"])
    # automatically figure out whether to encrypt or decrypt the folder
    if status["encrypted"]:
        print("Files are encrypted, decrypting...")
        action = decrypt_file
        msg = "decrypted folder"
        encrypted = False
    else:
        print("Files are not encrypted, encrypting...")
        action = encrypt_file
        msg = "encrypted folder"
        encrypted = True

    recursive_file_action(settings.ENCRYPT_FOLDER_PATH,
                          action, key)
    # log and set new encrypted status
    status_manager.log_activity(msg)
    status_manager.update("encrypted", encrypted)
