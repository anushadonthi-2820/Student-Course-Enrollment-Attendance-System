import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


# You can later use this for a login system if you want.
DEFAULT_ADMIN_USER = "admin"
DEFAULT_ADMIN_HASH = hash_password("admin123")
