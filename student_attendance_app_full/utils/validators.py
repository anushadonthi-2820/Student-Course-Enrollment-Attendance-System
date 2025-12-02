import re
from .helpers import parse_date


def validate_non_empty(value: str, field_name: str) -> str | None:
    if not value.strip():
        return f"{field_name} cannot be empty."
    return None


def validate_email(email: str) -> str | None:
    if not email:
        return None  # optional
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        return "Invalid email format."
    return None


def validate_date_str(date_str: str) -> str | None:
    if not parse_date(date_str):
        return "Date must be in YYYY-MM-DD format."
    return None
