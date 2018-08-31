TEST_MODE = True
# provide a file for test mode instead of recursively encrypting everything
ENCRYPT_FOLDER_PATH = "test_folder" if TEST_MODE else "asdf"

STATUS_FILE_PATH = "status.json"
LOG_FILE_PATH = "logs"

HASH_ITERATIONS = 500000
CHECK_PHRASE = b"lorem ipsum"
