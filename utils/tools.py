import re


def is_url(text: str) -> bool:
    return bool(re.match(r'^https?://', text.strip(), re.IGNORECASE))