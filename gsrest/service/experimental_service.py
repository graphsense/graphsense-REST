import gsrest.service.common_service as common
from gsrest.service.addresses_service import list_tags_by_address
from gsrest.service.entities_service import (
    list_address_tags_by_entity_internal, PAGE_SIZE_GET_ALL_TAGS)
from gsrest.util.tag_summary import get_tag_summary
from functools import partial
from gsrest.service.common_service import cannonicalize_address
from gsrest.service.tags_service import address_tag_from_row
from gsrest.db.util import tagstores


async def get_tag_summary_by_address(request, currency, address):
    address_canonical = cannonicalize_address(currency, address)
    db = request.app['db']

    entity_id = await db.get_address_entity_id(currency, address_canonical)

    tags = await tagstores(request.app['tagstores'], address_tag_from_row,
                           'get_best_entity_tag', currency, entity_id,
                           request.app['request_config']['show_private_tags'])

    next_page_fn = partial(list_tags_by_address, request, currency,
                           address_canonical)
    return await get_tag_summary(next_page_fn, additional_tags=tags)


async def get_tag_summary_by_entity(request, currency, entity):
    next_page_fn = partial(list_address_tags_by_entity_internal,
                           request,
                           currency,
                           entity,
                           pagesize=PAGE_SIZE_GET_ALL_TAGS)
    return await get_tag_summary(next_page_fn)


async def get_address(request, currency, address):
    return await common.get_address(request, currency, address)
