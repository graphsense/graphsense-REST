"""Slim Pydantic models for the GraphSense REST API.

This module provides the API response models as native Pydantic v2 models,
replacing the generated OpenAPI models with a clean, minimal implementation.
"""

from gsrest.models.addresses import Address, NeighborAddress, NeighborAddresses
from gsrest.models.base import APIModel
from gsrest.models.blocks import Block, BlockAtDate
from gsrest.models.common import LabeledItemRef
from gsrest.models.entities import (
    Entity,
    EntityAddresses,
    NeighborEntities,
    NeighborEntity,
)
from gsrest.models.general import (
    Actor,
    ActorContext,
    Concept,
    CurrencyStats,
    ExternalConversion,
    Rates,
    RelatedAddress,
    RelatedAddresses,
    Stats,
    Taxonomy,
    TokenConfig,
    TokenConfigs,
)
from gsrest.models.search import (
    SearchResult,
    SearchResultByCurrency,
    SearchResultLeaf,
    SearchResultLevel1,
    SearchResultLevel2,
    SearchResultLevel3,
    SearchResultLevel4,
    SearchResultLevel5,
    SearchResultLevel6,
)
from gsrest.models.tags import (
    AddressTag,
    AddressTags,
    LabelSummary,
    Tag,
    TagCloudEntry,
    TagSummary,
    UserTagReportResponse,
)
from gsrest.models.transactions import (
    AddressTxs,
    AddressTxUtxo,
    Link,
    LinkUtxo,
    Links,
    Tx,
    TxAccount,
    TxRef,
    Txs,
    TxSummary,
    TxUtxo,
    TxValue,
)
from gsrest.models.values import Rate, Values

__all__ = [
    # Base
    "APIModel",
    # Common
    "LabeledItemRef",
    # Values
    "Rate",
    "Values",
    # Transactions
    "TxSummary",
    "TxRef",
    "TxValue",
    "TxUtxo",
    "TxAccount",
    "Tx",
    "Txs",
    "AddressTxUtxo",
    "AddressTxs",
    "LinkUtxo",
    "Link",
    "Links",
    # Tags
    "Tag",
    "AddressTag",
    "AddressTags",
    "TagCloudEntry",
    "LabelSummary",
    "TagSummary",
    "UserTagReportResponse",
    # Addresses
    "Address",
    "NeighborAddress",
    "NeighborAddresses",
    # Entities
    "Entity",
    "NeighborEntity",
    "NeighborEntities",
    "EntityAddresses",
    # Blocks
    "Block",
    "BlockAtDate",
    # Search
    "SearchResultByCurrency",
    "SearchResult",
    "SearchResultLeaf",
    "SearchResultLevel1",
    "SearchResultLevel2",
    "SearchResultLevel3",
    "SearchResultLevel4",
    "SearchResultLevel5",
    "SearchResultLevel6",
    # General
    "CurrencyStats",
    "Stats",
    "Rates",
    "Taxonomy",
    "Concept",
    "ActorContext",
    "Actor",
    "TokenConfig",
    "TokenConfigs",
    "RelatedAddress",
    "RelatedAddresses",
    "ExternalConversion",
]
