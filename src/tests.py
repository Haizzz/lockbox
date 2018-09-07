import unittest
import base64

import encryption
import settings


class TestEncryption(unittest.TestCase):

    def setUp(self):
        self.test_folder = "test_folder"
        self.test_file = "{}/test.txt".format(self.test_folder)
        self.test_file_encrypted = self.test_file + settings.ENCRYPTED_FILE_EXTENSION
        self.key = base64.urlsafe_b64encode(
            b"a" * 32)  # Fernet requires 32 bytes key

    def test_encrypt_decrypt_file(self):
        # test encrypting and decrypting a single file
        # get current value in the file
        content = None
        with open(self.test_file, "rb") as f:
            content = f.read()
        # file content should now be different
        encryption.encrypt_file(self.test_file, self.key)
        new_content = None
        with open(self.test_file_encrypted, "rb") as f:
            new_content = f.read()
        self.assertFalse(content == new_content)
        # decrypt and the content should be reverted
        encryption.decrypt_file(self.test_file_encrypted, self.key)
        new_content = None
        with open(self.test_file, "rb") as f:
            new_content = f.read()
        self.assertEqual(content, new_content)


if __name__ == '__main__':
    unittest.main()
