from cryptography.fernet import Fernet
import os
import base64

class DataEncryption:
    # In production, load this from a secure vault or env variable
    _key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())
    _cipher_suite = Fernet(_key.encode())

    @classmethod
    def encrypt(cls, data: bytes) -> bytes:
        """Encrypts raw bytes."""
        return cls._cipher_suite.encrypt(data)

    @classmethod
    def decrypt(cls, encrypted_data: bytes) -> bytes:
        """Decrypts to raw bytes."""
        return cls._cipher_suite.decrypt(encrypted_data)
