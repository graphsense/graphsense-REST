from gsrest.dependencies import get_service_container, get_tagstore_access_groups
from gsrest.translators import (
    pydantic_search_result_by_currency_to_openapi,
    pydantic_search_result_to_openapi,
    pydantic_stats_to_openapi,
)


async def get_statistics(request):
    """Returns summary statistics on all available currencies"""
    services = get_service_container(request)
    version = request.app["openapi"]["info"]["version"]

    pydantic_result = await services.general_service.get_statistics(version)

    return pydantic_stats_to_openapi(pydantic_result)


async def search_by_currency(request, currency, q, limit=10):
    services = get_service_container(request)

    pydantic_result = await services.general_service.search_by_currency(
        currency, q, limit
    )

    return pydantic_search_result_by_currency_to_openapi(pydantic_result)


async def search(request, q, currency=None, limit=10, include_sub_tx_identifiers=False):
    services = get_service_container(request)
    tagstore_groups = get_tagstore_access_groups(request)

    pydantic_result = await services.general_service.search(
        q,
        tagstore_groups,
        currency,
        limit,
        include_sub_tx_identifiers=include_sub_tx_identifiers,
    )

    return pydantic_search_result_to_openapi(pydantic_result)
