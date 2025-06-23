import hashlib


def hash_(text):
    text_bytes = text.encode("utf-8")
    sha256_hash = hashlib.sha256()
    sha256_hash.update(text_bytes)
    hash_object = sha256_hash.hexdigest()
    return hash_object

