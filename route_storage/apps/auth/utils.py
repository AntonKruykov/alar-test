import hashlib

def encode_password(password: str) -> str:
    """Encode user password for store in db."""
    return str(hashlib.md5(password.encode()).hexdigest())
