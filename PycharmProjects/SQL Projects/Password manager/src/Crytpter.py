import hashlib
import base64
from BD_data_access import readcell


def hash_(text):
    text_bytes = text.encode("utf-8")
    sha256_hash = hashlib.sha256()
    sha256_hash.update(text_bytes)
    hash_object = sha256_hash.hexdigest()
    return hash_object


# Clé sous forme hexadécimale (par ex. hash SHA-256)
def hex_key_to_bytes_key(hex_key):
    key_bytes = bytes.fromhex(hex_key)
    return key_bytes


def xor_crypt(data: bytes, key) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])


def crypt(message: str) -> str:
    key = hex_key_to_bytes_key(readcell(1, 2))
    data = message.encode()
    encrypted = xor_crypt(data, key)
    return base64.b64encode(encrypted).decode()


def decrypt(encoded: str) -> str:
    key = hex_key_to_bytes_key(readcell(1, 2))
    try:

        data = base64.b64decode(encoded)
        decrypted = xor_crypt(data, key)
        return decrypted.decode()


    except (UnicodeDecodeError, ValueError):
        return "Invalid key"
