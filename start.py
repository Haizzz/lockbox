# contain functions to setup lockbox in a new folder
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def setup() -> dict:
    """
    Set a password for this folder,
    return the salt and password hash in a dictionary
    :return: dict
    """
    # https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
    password = input("New password: ").encode()
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    hashed_password = base64.urlsafe_b64encode(kdf.derive(password))
    return {
        "salt": salt.hex(),
        "hashed_password": hashed_password.hex()
    }


"""
{
    "password_set": false,
    "salt": "",
    "hashed_password": ""
}
"""
