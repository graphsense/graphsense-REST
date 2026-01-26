"""Common API models shared across domains."""

from gsrest.models.base import APIModel


class LabeledItemRef(APIModel):
    """Reference to a labeled item."""

    id: str
    label: str
