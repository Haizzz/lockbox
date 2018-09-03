# provide high level encryption methods
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
import logging
from tqdm import tqdm

import settings

logger = logging.getLogger()


def encrypt_file(path, key):
    """
    Encrypt a file's content

    :param path: string path to file
    :param key: byte string encryption key
    :return: None
    """
    # if file ends in encrypted file extension, skip
    if os.path.splitext(path)[1] == settings.ENCRYPTED_FILE_EXTENSION:
        return
    f = Fernet(key)
    # keep reading, encrypting and writting to file separate
    # incase encyrpting fail file doesn't get truncated
    # read
    try:
        with open(path, "rb") as file:
            file_content = file.read()
        # encrypt
        cypher = f.encrypt(file_content)
        # write to file
        with open(path, "wb") as file:
            file.write(cypher)
    except PermissionError:
        # not enough permission, skip
        return
    except FileNotFoundError:
        # file is an alias, skip
        return
    # rename the file with encrypted file extension
    os.rename(path, path + settings.ENCRYPTED_FILE_EXTENSION)


def decrypt_file(path, key):
    """
    Decrypt a file's content

    :param path: string path to file
    :param key: byte string encryption key
    :return: None
    """
    # if file extension does not end with encrypted file extension, skip
    if os.path.splitext(path)[1] != settings.ENCRYPTED_FILE_EXTENSION:
        return
    f = Fernet(key)
    # keep reading, decrypting and writting to file separate
    # incase decrypting fail file doesn't get truncated
    # read
    try:
        with open(path, "rb") as file:
            file_content = file.read()
        # decrypt
        text = f.decrypt(file_content)
        # write to file
        with open(path, "wb") as file:
            file.write(text)
        # remove encrypted file extension from file
        path_components = os.path.split(path)
    except PermissionError:
        # not enough permission, skip
        return
    except FileNotFoundError:
        # file is an alias, skip
        return
    os.rename(
        path,
        os.path.join(
            path_components[0], os.path.splitext(path_components[1])[0]
        )
    )


def generate_key_from_password(pwd, salt=None):
    """
    Generate a Fernet key from a given password string
    :param pwd: string password input
    :param salt: byte object salt to add
    :return: byte object
    """
    # https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
    password = base64.urlsafe_b64encode(pwd.encode())
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=settings.HASH_ITERATIONS,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def check_correct_password(status, pwd):
    """
    Attempt to decrypt encrypted_check_phrase and check it
    against the check phrase to see if the password is the same. This is to
    avoid user inputting wrong password and accidentally corrupting the
    data by decrypting it with the wrong key

    :param status: dictionary of the current status
    :param pwd: string input password to check with
    :return: boolean
    """
    # generate key from raw password
    key = generate_key_from_password(
        pwd, salt=status.get("salt")
    )
    f = Fernet(key)
    try:
        decrypt_output = f.decrypt(status["encrypted_check_phrase"])
    except InvalidToken:
        return False
    return decrypt_output.decode("utf-8") != settings.CHECK_PHRASE


def recursive_file_action(path, fx, *args, **kwargs):
    """
    Recursively run function fx on all files within path
    including all files in subdirectories recursively. The file
    path will be passed to fx along with args and kwargs

    :param path: string path to work on
    :param fx: function to run on each file
    :param args: passed to fx
    :param kwargs: passed to fx
    :return: None
    """
    # generate list of files to encrypt and encrypt separately
    # to make a pretty progress bar
    file_paths = []
    print("Collecting files...")
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            # construct file path
            file_path = os.path.join(dirpath, filename)
            file_paths.append(file_path)
    print("Running process...")
    for path in tqdm(file_paths):
        # don't encrypt itself or data files
        if path not in settings.DONT_ENCRYPT:
            fx(path, *args, **kwargs)


def check_folder_fully_decrypted(path):
    """
    Go through all files in the given path and check if
    they're all decrypted (does not have encrypted file extension)

    :param path: str the path to check
    :return: boolean
    """
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if os.path.splitext(filename)[1] == settings.ENCRYPTED_FILE_EXTENSION:
                return False
    return True
