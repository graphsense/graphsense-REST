from graphsenselib.errors import BadUserInputException

from gsrest.dependencies import (
    get_request_cache,
    get_service_container,
    get_tagstore_access_groups,
)
from gsrest.translators import (
    pydantic_to_openapi,
)

# Updated functions using new service layer


async def list_related_addresses(
    request,
    currency: str,
    address: str,
    address_relation_type: str,
    page: str,
    pagesize: int,
):
    services = get_service_container(request)

    if address_relation_type not in ["pubkey", "all"]:
        raise BadUserInputException(
            "Invalid address_relation_type. Must be 'pubkey' or 'all'."
        )

    pydantic_result = (
        await services.addresses_service.get_cross_chain_pubkey_related_addresses(
            address, network=currency
        )
    )

    return pydantic_to_openapi(pydantic_result)


async def get_tag_summary_by_address(
    request, currency, address, include_best_cluster_tag=False
):
    services = get_service_container(request)
    tagstore_groups = get_tagstore_access_groups(request)

    pydantic_result = await services.addresses_service.get_tag_summary_by_address(
        currency, address, tagstore_groups, include_best_cluster_tag
    )

    return pydantic_to_openapi(pydantic_result)


async def get_address(request, currency, address, include_actors=True):
    services = get_service_container(request)
    tagstore_groups = get_tagstore_access_groups(request)

    pydantic_result = await services.addresses_service.get_address(
        currency, address, tagstore_groups, include_actors
    )

    return pydantic_to_openapi(pydantic_result)


async def list_tags_by_address(
    request, currency, address, page=None, pagesize=None, include_best_cluster_tag=False
):
    services = get_service_container(request)
    tagstore_groups = get_tagstore_access_groups(request)
    cache = get_request_cache(request)

    pydantic_result = await services.addresses_service.list_tags_by_address(
        currency,
        address,
        tagstore_groups,
        cache,
        page,
        pagesize,
        include_best_cluster_tag,
    )

    return pydantic_to_openapi(pydantic_result)


async def list_address_txs(
    request,
    currency,
    address,
    min_height=None,
    max_height=None,
    min_date=None,
    max_date=None,
    direction=None,
    order="desc",
    token_currency=None,
    page=None,
    pagesize=None,
):
    services = get_service_container(request)

    pydantic_result = await services.addresses_service.list_address_txs(
        currency,
        address,
        min_height,
        max_height,
        min_date,
        max_date,
        direction,
        order,
        token_currency,
        page,
        pagesize,
    )

    return pydantic_to_openapi(pydantic_result)


async def list_address_neighbors(
    request,
    currency,
    address,
    direction,
    only_ids=None,
    include_labels=False,
    include_actors=True,
    page=None,
    pagesize=None,
):
    services = get_service_container(request)
    tagstore_groups = get_tagstore_access_groups(request)

    pydantic_result = await services.addresses_service.list_address_neighbors(
        currency,
        address,
        direction,
        tagstore_groups,
        only_ids,
        include_labels,
        include_actors,
        page,
        pagesize,
    )

    return pydantic_to_openapi(pydantic_result)


async def list_address_links(
    request,
    currency,
    address,
    neighbor,
    min_height=None,
    max_height=None,
    min_date=None,
    max_date=None,
    order="desc",
    token_currency=None,
    page=None,
    pagesize=None,
):
    services = get_service_container(request)
    request_timeout = request.app["config"].address_links_request_timeout

    pydantic_result = await services.addresses_service.list_address_links(
        currency,
        address,
        neighbor,
        min_height,
        max_height,
        min_date,
        max_date,
        order,
        token_currency,
        page,
        pagesize,
        request_timeout,
    )

    return pydantic_to_openapi(pydantic_result)


async def get_address_entity(request, currency, address, include_actors=True):
    services = get_service_container(request)
    tagstore_groups = get_tagstore_access_groups(request)

    pydantic_result = await services.addresses_service.get_address_entity(
        currency, address, include_actors, tagstore_groups
    )

    return pydantic_to_openapi(pydantic_result)
