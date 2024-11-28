import re

pattern = re.compile(r"[\W_]+", re.UNICODE)  # alphanumeric chars for label


def alphanumeric_lower(expression):
    return pattern.sub("", expression).lower()


def remove_prefix(s: str, prefix: str) -> str:
    if s.startswith(prefix):
        return s[len(prefix) :]
    else:
        return s
