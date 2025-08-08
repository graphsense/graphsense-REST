from typing import Union

from gsrest.services.models import Actor as PydanticActor
from gsrest.services.models import ActorContext as PydanticActorContext
from gsrest.services.models import (
    Address as PydanticAddress,
)
from gsrest.services.models import (
    AddressTag as PydanticAddressTag,
)
from gsrest.services.models import (
    AddressTagResult as PydanticAddressTagResult,
)
from gsrest.services.models import (
    AddressTxs as PydanticAddressTxs,
)
from gsrest.services.models import AddressTxUtxo as PydanticAddressTxUtxo
from gsrest.services.models import (
    Block as PydanticBlock,
)
from gsrest.services.models import (
    BlockAtDate as PydanticBlockAtDate,
)
from gsrest.services.models import Concept as PydanticConcept
from gsrest.services.models import (
    CurrencyStats as PydanticCurrencyStats,
)
from gsrest.services.models import (
    Entity as PydanticEntity,
)
from gsrest.services.models import (
    EntityAddresses as PydanticEntityAddresses,
)
from gsrest.services.models import ExternalConversions as PydanticExternalConversions
from gsrest.services.models import (
    LabeledItemRef as PydanticLabeledItemRef,
)
from gsrest.services.models import LabelSummary as PydanticLabelSummary
from gsrest.services.models import (
    Links as PydanticLinks,
)
from gsrest.services.models import LinkUtxo as PydanticLinkUtxo
from gsrest.services.models import NeighborAddress as PydanticNeighborAddress
from gsrest.services.models import NeighborAddresses as PydanticNeighborAddresses
from gsrest.services.models import NeighborEntities as PydanticNeighborEntities
from gsrest.services.models import NeighborEntity as PydanticNeighborEntity
from gsrest.services.models import (
    RatesResponse as PydanticRates,
)
from gsrest.services.models import (
    SearchResult as PydanticSearchResult,
)
from gsrest.services.models import (
    SearchResultByCurrency as PydanticSearchResultByCurrency,
)
from gsrest.services.models import (
    Stats as PydanticStats,
)
from gsrest.services.models import TagCloudEntry as PydanticTagCloudEntry
from gsrest.services.models import TagSummary as PydanticTagSummary
from gsrest.services.models import Taxonomy as PydanticTaxonomy
from gsrest.services.models import (
    TokenConfigs as PydanticTokenConfigs,
)
from gsrest.services.models import (
    TxAccount as PydanticTxAccount,
)
from gsrest.services.models import (
    TxRef as PydanticTxRef,
)
from gsrest.services.models import (
    TxSummary as PydanticTxSummary,
)
from gsrest.services.models import (
    TxUtxo as PydanticTxUtxo,
)
from gsrest.services.models import (
    TxValue as PydanticTxValue,
)
from gsrest.services.models import (
    Values as PydanticValues,
)
from openapi_server.models.actor import Actor
from openapi_server.models.actor_context import ActorContext
from openapi_server.models.address import Address
from openapi_server.models.address_tag import AddressTag
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.address_tx_utxo import AddressTxUtxo
from openapi_server.models.address_txs import AddressTxs
from openapi_server.models.block import Block
from openapi_server.models.block_at_date import BlockAtDate
from openapi_server.models.concept import Concept
from openapi_server.models.currency_stats import CurrencyStats
from openapi_server.models.entity import Entity
from openapi_server.models.entity_addresses import EntityAddresses
from openapi_server.models.external_conversions import ExternalConversions
from openapi_server.models.label_summary import LabelSummary
from openapi_server.models.labeled_item_ref import LabeledItemRef
from openapi_server.models.link_utxo import LinkUtxo
from openapi_server.models.links import Links
from openapi_server.models.neighbor_address import NeighborAddress
from openapi_server.models.neighbor_addresses import NeighborAddresses
from openapi_server.models.neighbor_entities import NeighborEntities
from openapi_server.models.neighbor_entity import NeighborEntity
from openapi_server.models.rates import Rates
from openapi_server.models.search_result import SearchResult
from openapi_server.models.search_result_by_currency import SearchResultByCurrency
from openapi_server.models.stats import Stats
from openapi_server.models.tag_cloud_entry import TagCloudEntry
from openapi_server.models.tag_summary import TagSummary
from openapi_server.models.taxonomy import Taxonomy
from openapi_server.models.token_config import TokenConfig
from openapi_server.models.token_configs import TokenConfigs
from openapi_server.models.tx import Tx
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.tx_ref import TxRef
from openapi_server.models.tx_summary import TxSummary
from openapi_server.models.tx_utxo import TxUtxo
from openapi_server.models.tx_value import TxValue
from openapi_server.models.values import Values


def pydantic_token_configs_to_openapi(
    pydantic_configs: PydanticTokenConfigs,
) -> TokenConfigs:
    """Convert Pydantic TokenConfigs to OpenAPI TokenConfigs"""
    return TokenConfigs(
        [
            TokenConfig(
                ticker=config.ticker,
                decimals=config.decimals,
                peg_currency=config.peg_currency,
                contract_address=config.contract_address,
            )
            for config in pydantic_configs.token_configs
        ]
    )


def pydantic_currency_stats_to_openapi(
    pydantic_stats: PydanticCurrencyStats,
) -> CurrencyStats:
    """Convert Pydantic CurrencyStats to OpenAPI CurrencyStats"""
    return CurrencyStats.from_dict(pydantic_stats.model_dump())


def pydantic_tx_value_to_openapi(pydantic_tx_value: PydanticTxValue) -> TxValue:
    """Convert Pydantic TxValue to OpenAPI TxValue"""
    return TxValue(
        address=pydantic_tx_value.address,
        value=pydantic_values_to_openapi(pydantic_tx_value.value),
        index=pydantic_tx_value.index,
    )


def pydantic_tx_ref_to_openapi(pydantic_tx_ref: PydanticTxRef) -> TxRef:
    """Convert Pydantic TxRef to OpenAPI TxRef"""
    return TxRef.from_dict(pydantic_tx_ref.model_dump())


def pydantic_tx_account_to_openapi(pydantic_tx: PydanticTxAccount) -> TxAccount:
    """Convert Pydantic TxAccount to OpenAPI TxAccount"""
    return TxAccount(
        currency=pydantic_tx.currency,
        network=pydantic_tx.network,
        tx_type=pydantic_tx.tx_type,
        identifier=pydantic_tx.identifier,
        tx_hash=pydantic_tx.tx_hash,
        timestamp=pydantic_tx.timestamp,
        height=pydantic_tx.height,
        from_address=pydantic_tx.from_address,
        to_address=pydantic_tx.to_address,
        token_tx_id=pydantic_tx.token_tx_id,
        contract_creation=pydantic_tx.contract_creation,
        value=pydantic_values_to_openapi(pydantic_tx.value),
    )


def pydantic_tx_utxo_to_openapi(pydantic_tx: PydanticTxUtxo) -> TxUtxo:
    """Convert Pydantic TxUtxo to OpenAPI TxUtxo"""
    return TxUtxo(
        currency=pydantic_tx.currency,
        tx_hash=pydantic_tx.tx_hash,
        coinbase=pydantic_tx.coinbase,
        height=pydantic_tx.height,
        no_inputs=pydantic_tx.no_inputs,
        no_outputs=pydantic_tx.no_outputs,
        inputs=[pydantic_tx_value_to_openapi(inp) for inp in (pydantic_tx.inputs or [])]
        if pydantic_tx.inputs
        else None,
        outputs=[
            pydantic_tx_value_to_openapi(out) for out in (pydantic_tx.outputs or [])
        ]
        if pydantic_tx.outputs
        else None,
        timestamp=pydantic_tx.timestamp,
        total_input=pydantic_values_to_openapi(pydantic_tx.total_input),
        total_output=pydantic_values_to_openapi(pydantic_tx.total_output),
    )


def pydantic_rates_to_openapi(pydantic_rates: PydanticRates) -> Rates:
    """Convert Pydantic Rates to OpenAPI Rates"""
    return Rates.from_dict(pydantic_rates.model_dump())


def pydantic_values_to_openapi(pydantic_values: PydanticValues) -> Values:
    """Convert Pydantic Values to OpenAPI Values"""
    return Values.from_dict(pydantic_values.model_dump())


def pydantic_tx_summary_to_openapi(pydantic_tx: PydanticTxSummary) -> TxSummary:
    """Convert Pydantic TxSummary to OpenAPI TxSummary"""
    return TxSummary.from_dict(pydantic_tx.model_dump())


def pydantic_labeled_item_ref_to_openapi(
    pydantic_ref: PydanticLabeledItemRef,
) -> LabeledItemRef:
    """Convert Pydantic LabeledItemRef to OpenAPI LabeledItemRef"""
    return LabeledItemRef.from_dict(pydantic_ref.model_dump())


def pydantic_address_tag_to_openapi(pydantic_tag: PydanticAddressTag) -> AddressTag:
    """Convert Pydantic AddressTag to OpenAPI AddressTag"""
    return AddressTag(
        address=pydantic_tag.address,
        entity=pydantic_tag.entity,
        category=pydantic_tag.category,
        concepts=pydantic_tag.concepts,
        actor=pydantic_tag.actor,
        tag_type=pydantic_tag.tag_type,
        abuse=pydantic_tag.abuse,
        label=pydantic_tag.label,
        lastmod=pydantic_tag.lastmod,
        source=pydantic_tag.source,
        tagpack_is_public=pydantic_tag.tagpack_is_public,
        tagpack_uri=pydantic_tag.tagpack_uri,
        tagpack_creator=pydantic_tag.tagpack_creator,
        tagpack_title=pydantic_tag.tagpack_title,
        confidence=pydantic_tag.confidence,
        confidence_level=pydantic_tag.confidence_level,
        is_cluster_definer=pydantic_tag.is_cluster_definer,
        inherited_from=pydantic_tag.inherited_from,
        currency=pydantic_tag.currency,
    )


def pydantic_address_to_openapi(pydantic_address: PydanticAddress) -> Address:
    """Convert Pydantic Address to OpenAPI Address"""
    return Address(
        address=pydantic_address.address,
        currency=pydantic_address.currency,
        entity=pydantic_address.entity,
        first_tx=pydantic_tx_summary_to_openapi(pydantic_address.first_tx)
        if pydantic_address.first_tx
        else None,
        last_tx=pydantic_tx_summary_to_openapi(pydantic_address.last_tx)
        if pydantic_address.last_tx
        else None,
        no_incoming_txs=pydantic_address.no_incoming_txs,
        no_outgoing_txs=pydantic_address.no_outgoing_txs,
        total_received=pydantic_values_to_openapi(pydantic_address.total_received),
        total_tokens_received={
            k: pydantic_values_to_openapi(v)
            for k, v in (pydantic_address.total_tokens_received or {}).items()
        }
        if pydantic_address.total_tokens_received
        else None,
        total_spent=pydantic_values_to_openapi(pydantic_address.total_spent),
        total_tokens_spent={
            k: pydantic_values_to_openapi(v)
            for k, v in (pydantic_address.total_tokens_spent or {}).items()
        }
        if pydantic_address.total_tokens_spent
        else None,
        in_degree=pydantic_address.in_degree,
        out_degree=pydantic_address.out_degree,
        balance=pydantic_values_to_openapi(pydantic_address.balance),
        token_balances={
            k: pydantic_values_to_openapi(v)
            for k, v in (pydantic_address.token_balances or {}).items()
        }
        if pydantic_address.token_balances
        else None,
        is_contract=pydantic_address.is_contract,
        actors=[
            pydantic_labeled_item_ref_to_openapi(actor)
            for actor in (pydantic_address.actors or [])
        ]
        if pydantic_address.actors
        else None,
        status=pydantic_address.status,
    )


def pydantic_entity_to_openapi(pydantic_entity: PydanticEntity) -> Entity:
    """Convert Pydantic Entity to OpenAPI Entity"""
    return Entity(
        currency=pydantic_entity.currency,
        entity=pydantic_entity.entity,
        root_address=pydantic_entity.root_address,
        first_tx=pydantic_tx_summary_to_openapi(pydantic_entity.first_tx),
        last_tx=pydantic_tx_summary_to_openapi(pydantic_entity.last_tx),
        no_addresses=pydantic_entity.no_addresses,
        no_incoming_txs=pydantic_entity.no_incoming_txs,
        no_outgoing_txs=pydantic_entity.no_outgoing_txs,
        total_received=pydantic_values_to_openapi(pydantic_entity.total_received),
        total_tokens_received={
            k: pydantic_values_to_openapi(v)
            for k, v in (pydantic_entity.total_tokens_received or {}).items()
        }
        if pydantic_entity.total_tokens_received
        else None,
        total_spent=pydantic_values_to_openapi(pydantic_entity.total_spent),
        total_tokens_spent={
            k: pydantic_values_to_openapi(v)
            for k, v in (pydantic_entity.total_tokens_spent or {}).items()
        }
        if pydantic_entity.total_tokens_spent
        else None,
        in_degree=pydantic_entity.in_degree,
        out_degree=pydantic_entity.out_degree,
        balance=pydantic_values_to_openapi(pydantic_entity.balance),
        token_balances={
            k: pydantic_values_to_openapi(v)
            for k, v in (pydantic_entity.token_balances or {}).items()
        }
        if pydantic_entity.token_balances
        else None,
        best_address_tag=pydantic_address_tag_to_openapi(
            pydantic_entity.best_address_tag
        )
        if pydantic_entity.best_address_tag
        else None,
        no_address_tags=pydantic_entity.no_address_tags,
        actors=[
            pydantic_labeled_item_ref_to_openapi(actor)
            for actor in (pydantic_entity.actors or [])
        ]
        if pydantic_entity.actors
        else None,
    )


def pydantic_entity_addresses_to_openapi(
    pydantic_result: PydanticEntityAddresses,
) -> EntityAddresses:
    """Convert Pydantic EntityAddresses to OpenAPI EntityAddresses"""
    return EntityAddresses(
        next_page=pydantic_result.next_page,
        addresses=[
            pydantic_address_to_openapi(addr) for addr in pydantic_result.addresses
        ],
    )


def pydantic_address_tag_result_to_openapi(
    pydantic_result: PydanticAddressTagResult,
) -> AddressTags:
    """Convert Pydantic AddressTagResult to OpenAPI AddressTags"""
    return AddressTags(
        next_page=pydantic_result.next_page,
        address_tags=[
            pydantic_address_tag_to_openapi(tag) for tag in pydantic_result.address_tags
        ],
    )


def pydantic_address_txs_to_openapi(pydantic_txs: PydanticAddressTxs) -> AddressTxs:
    """Convert Pydantic AddressTxs to OpenAPI AddressTxs"""

    # Use model_dump and from_dict to handle the inheritance complexity
    txs_data = pydantic_txs.model_dump()

    return AddressTxs.from_dict(txs_data)


def pydantic_tx_to_openapi(
    pydantic_txs: Union[PydanticTxAccount, PydanticTxUtxo],
) -> AddressTxs:
    """Convert Pydantic Tx to OpenAPI AddressTxs"""

    # Use model_dump and from_dict to handle the inheritance complexity
    txs_data = pydantic_txs.model_dump()

    return Tx.from_dict(txs_data)


def pydantic_link_utxo_to_openapi(pydantic_link: PydanticLinkUtxo) -> LinkUtxo:
    """Convert Pydantic LinkUtxo to OpenAPI LinkUtxo"""
    return LinkUtxo(
        tx_hash=pydantic_link.tx_hash,
        height=pydantic_link.height,
        currency=pydantic_link.currency,
        timestamp=pydantic_link.timestamp,
        input_value=pydantic_values_to_openapi(pydantic_link.input_value),
        output_value=pydantic_values_to_openapi(pydantic_link.output_value),
    )


def pydantic_address_tx_utxo_to_openapi(
    pydantic_tx: PydanticAddressTxUtxo,
) -> AddressTxUtxo:
    """Convert Pydantic AddressTxUtxo to OpenAPI AddressTxUtxo"""
    return AddressTxUtxo(
        currency=pydantic_tx.currency,
        height=pydantic_tx.height,
        timestamp=pydantic_tx.timestamp,
        coinbase=pydantic_tx.coinbase,
        tx_hash=pydantic_tx.tx_hash,
        value=pydantic_values_to_openapi(pydantic_tx.value),
    )


def pydantic_links_to_openapi(pydantic_links: PydanticLinks) -> Links:
    """Convert Pydantic Links to OpenAPI Links"""
    # Handle mixed link types
    openapi_links = []
    for link in pydantic_links.links:
        if isinstance(link, PydanticLinkUtxo):
            openapi_links.append(pydantic_link_utxo_to_openapi(link))
        elif isinstance(link, PydanticAddressTxUtxo):
            openapi_links.append(pydantic_address_tx_utxo_to_openapi(link))
        elif isinstance(link, PydanticTxAccount):
            openapi_links.append(pydantic_tx_account_to_openapi(link))
        else:
            raise NotImplementedError(
                f"Unsupported link type: {type(link)}"
            )

    return Links(next_page=pydantic_links.next_page, links=openapi_links)


def pydantic_block_to_openapi(pydantic_block: PydanticBlock) -> Block:
    """Convert Pydantic Block to OpenAPI Block"""
    return Block(
        currency=pydantic_block.currency,
        height=pydantic_block.height,
        block_hash=pydantic_block.block_hash,
        no_txs=pydantic_block.no_txs,
        timestamp=pydantic_block.timestamp,
    )


def pydantic_block_at_date_to_openapi(
    pydantic_block_at_date: PydanticBlockAtDate,
) -> BlockAtDate:
    """Convert Pydantic BlockAtDate to OpenAPI BlockAtDate"""
    return BlockAtDate(
        before_block=pydantic_block_at_date.before_block,
        before_timestamp=pydantic_block_at_date.before_timestamp,
        after_block=pydantic_block_at_date.after_block,
        after_timestamp=pydantic_block_at_date.after_timestamp,
    )


def pydantic_stats_to_openapi(pydantic_stats: PydanticStats) -> Stats:
    """Convert Pydantic Stats to OpenAPI Stats"""
    return Stats(
        currencies=[
            pydantic_currency_stats_to_openapi(cs) for cs in pydantic_stats.currencies
        ],
        version=pydantic_stats.version,
        request_timestamp=pydantic_stats.request_timestamp,
    )


def pydantic_search_result_by_currency_to_openapi(
    pydantic_result: PydanticSearchResultByCurrency,
) -> SearchResultByCurrency:
    """Convert Pydantic SearchResultByCurrency to OpenAPI SearchResultByCurrency"""
    return SearchResultByCurrency(
        currency=pydantic_result.currency,
        addresses=pydantic_result.addresses,
        txs=pydantic_result.txs,
    )


def pydantic_search_result_to_openapi(
    pydantic_result: PydanticSearchResult,
) -> SearchResult:
    """Convert Pydantic SearchResult to OpenAPI SearchResult"""
    return SearchResult(
        currencies=[
            pydantic_search_result_by_currency_to_openapi(c)
            for c in pydantic_result.currencies
        ],
        labels=pydantic_result.labels,
        actors=[
            pydantic_labeled_item_ref_to_openapi(actor)
            for actor in pydantic_result.actors
        ],
    )


def pydantic_actor_context_to_openapi(
    pydantic_context: PydanticActorContext,
) -> ActorContext:
    """Convert Pydantic ActorContext to OpenAPI ActorContext"""
    return ActorContext(
        uris=pydantic_context.uris,
        images=pydantic_context.images,
        refs=pydantic_context.refs,
        coingecko_ids=pydantic_context.coingecko_ids,
        defilama_ids=pydantic_context.defilama_ids,
        twitter_handle=pydantic_context.twitter_handle,
        github_organisation=pydantic_context.github_organisation,
        legal_name=pydantic_context.legal_name,
    )


def pydantic_actor_to_openapi(pydantic_actor: PydanticActor) -> Actor:
    """Convert Pydantic Actor to OpenAPI Actor"""
    return Actor(
        id=pydantic_actor.id,
        uri=pydantic_actor.uri,
        label=pydantic_actor.label,
        jurisdictions=[
            pydantic_labeled_item_ref_to_openapi(j)
            for j in pydantic_actor.jurisdictions
        ],
        categories=[
            pydantic_labeled_item_ref_to_openapi(c) for c in pydantic_actor.categories
        ],
        nr_tags=pydantic_actor.nr_tags,
        context=pydantic_actor_context_to_openapi(pydantic_actor.context)
        if pydantic_actor.context
        else None,
    )


def pydantic_concept_to_openapi(pydantic_concept: PydanticConcept) -> Concept:
    """Convert Pydantic Concept to OpenAPI Concept"""
    return Concept(
        id=pydantic_concept.id,
        label=pydantic_concept.label,
        description=pydantic_concept.description,
        taxonomy=pydantic_concept.taxonomy,
        uri=pydantic_concept.uri,
    )


def pydantic_taxonomy_to_openapi(pydantic_taxonomy: PydanticTaxonomy) -> Taxonomy:
    """Convert Pydantic Taxonomy to OpenAPI Taxonomy"""
    return Taxonomy(taxonomy=pydantic_taxonomy.taxonomy, uri=pydantic_taxonomy.uri)


def pydantic_external_conversions_to_openapi(
    pydantic_conversion: PydanticExternalConversions,
) -> ExternalConversions:
    """Convert Pydantic ExternalConversions to OpenAPI ExternalConversions"""
    return ExternalConversions(
        conversion_type=pydantic_conversion.conversion_type,
        from_address=pydantic_conversion.from_address,
        to_address=pydantic_conversion.to_address,
        from_asset=pydantic_conversion.from_asset,
        to_asset=pydantic_conversion.to_asset,
        from_amount=pydantic_conversion.from_amount,
        to_amount=pydantic_conversion.to_amount,
        from_asset_transfer=pydantic_conversion.from_asset_transfer,
        to_asset_transfer=pydantic_conversion.to_asset_transfer,
        from_network=pydantic_conversion.from_network,
        to_network=pydantic_conversion.to_network,
    )


def pydantic_tag_cloud_entry_to_openapi(
    pydantic_entry: PydanticTagCloudEntry,
) -> TagCloudEntry:
    """Convert Pydantic TagCloudEntry to OpenAPI TagCloudEntry"""
    return TagCloudEntry(cnt=pydantic_entry.cnt, weighted=pydantic_entry.weighted)


def pydantic_label_summary_to_openapi(
    pydantic_summary: PydanticLabelSummary,
) -> LabelSummary:
    """Convert Pydantic LabelSummary to OpenAPI LabelSummary"""
    return LabelSummary(
        label=pydantic_summary.label,
        count=pydantic_summary.count,
        confidence=pydantic_summary.confidence,
        relevance=pydantic_summary.relevance,
        creators=pydantic_summary.creators,
        sources=pydantic_summary.sources,
        concepts=pydantic_summary.concepts,
        lastmod=pydantic_summary.lastmod,
        inherited_from=pydantic_summary.inherited_from,
    )


def pydantic_tag_summary_to_openapi(pydantic_summary: PydanticTagSummary) -> TagSummary:
    """Convert Pydantic TagSummary to OpenAPI TagSummary"""
    return TagSummary(
        broad_category=pydantic_summary.broad_category,
        tag_count=pydantic_summary.tag_count,
        tag_count_indirect=pydantic_summary.tag_count_indirect,
        best_actor=pydantic_summary.best_actor,
        best_label=pydantic_summary.best_label,
        concept_tag_cloud={
            k: pydantic_tag_cloud_entry_to_openapi(v)
            for k, v in pydantic_summary.concept_tag_cloud.items()
        },
        label_summary={
            k: pydantic_label_summary_to_openapi(v)
            for k, v in pydantic_summary.label_summary.items()
        },
    )


def pydantic_neighbor_address_to_openapi(
    pydantic_neighbor: PydanticNeighborAddress,
) -> NeighborAddress:
    """Convert Pydantic NeighborAddress to OpenAPI NeighborAddress"""
    return NeighborAddress(
        labels=pydantic_neighbor.labels,
        value=pydantic_values_to_openapi(pydantic_neighbor.value),
        no_txs=pydantic_neighbor.no_txs,
        token_values={
            k: pydantic_values_to_openapi(v)
            for k, v in (pydantic_neighbor.token_values or {}).items()
        }
        if pydantic_neighbor.token_values
        else None,
        address=pydantic_address_to_openapi(pydantic_neighbor.address),
    )


def pydantic_neighbor_addresses_to_openapi(
    pydantic_neighbors: PydanticNeighborAddresses,
) -> NeighborAddresses:
    """Convert Pydantic NeighborAddresses to OpenAPI NeighborAddresses"""
    return NeighborAddresses(
        next_page=pydantic_neighbors.next_page,
        neighbors=[
            pydantic_neighbor_address_to_openapi(neighbor)
            for neighbor in pydantic_neighbors.neighbors
        ],
    )


def pydantic_neighbor_entities_to_openapi(
    pydantic_neighbors: PydanticNeighborEntities,
) -> NeighborEntities:
    """Convert Pydantic NeighborEntities to OpenAPI NeighborEntities"""
    return NeighborEntities(
        next_page=pydantic_neighbors.next_page,
        neighbors=[
            pydantic_neighbor_entity_to_openapi(neighbor)
            for neighbor in pydantic_neighbors.neighbors
        ],
    )


def pydantic_neighbor_entity_to_openapi(
    pydantic_neighbor: PydanticNeighborEntity,
) -> NeighborEntity:
    """Convert Pydantic NeighborEntity to OpenAPI NeighborEntity"""
    return NeighborEntity(
        labels=pydantic_neighbor.labels,
        value=pydantic_values_to_openapi(pydantic_neighbor.value),
        token_values={
            k: pydantic_values_to_openapi(v)
            for k, v in (pydantic_neighbor.token_values or {}).items()
        }
        if pydantic_neighbor.token_values
        else None,
        no_txs=pydantic_neighbor.no_txs,
        entity=pydantic_entity_to_openapi(pydantic_neighbor.entity)
        if isinstance(pydantic_neighbor.entity, PydanticEntity)
        else pydantic_neighbor.entity,
    )
