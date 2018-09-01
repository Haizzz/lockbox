import os
import sys

# get current directory path and current file name
if getattr(sys, 'frozen', False):
    name = sys.executable
    TEST_MODE = False
elif __file__:
    name = __file__
    TEST_MODE = True
APPLICATION_PATH = os.path.dirname(name)
APPLICATION_FILE_PATH = sys.executable

# provide a file for test mode instead of recursively encrypting everything
ENCRYPT_FOLDER_PATH = "test_folder" if TEST_MODE else APPLICATION_PATH

STATUS_FILE_PATH = os.path.join(APPLICATION_PATH, ".lockbox_status.json")
LOG_FILE_PATH = os.path.join(APPLICATION_PATH, ".lockbox_logs")

DONT_ENCRYPT = (  # path to files to ignore for encrypting
    APPLICATION_FILE_PATH,
    STATUS_FILE_PATH,
    LOG_FILE_PATH
)

HASH_ITERATIONS = 500000
CHECK_PHRASE = b"lorem ipsum"
