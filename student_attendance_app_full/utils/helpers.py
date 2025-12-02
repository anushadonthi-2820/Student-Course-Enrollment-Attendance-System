from datetime import datetime


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def parse_date(date_str: str) -> bool:
    """Return True if valid YYYY-MM-DD, else False."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
