import re

pattern = re.compile(r"[\W_]+", re.UNICODE)  # alphanumeric chars for label


def alphanumeric_lower(expression):
    return pattern.sub("", expression).lower()
