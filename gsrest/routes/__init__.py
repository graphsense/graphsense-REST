"""FastAPI routers for gsrest API endpoints"""

from gsrest.routes import (
    addresses,
    blocks,
    bulk,
    entities,
    general,
    rates,
    tags,
    tokens,
    txs,
)

__all__ = [
    "addresses",
    "blocks",
    "bulk",
    "entities",
    "general",
    "rates",
    "tags",
    "tokens",
    "txs",
]
