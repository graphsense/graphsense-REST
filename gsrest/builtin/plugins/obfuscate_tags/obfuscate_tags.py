from aiohttp import web
from openapi_server.models.entity import Entity
from openapi_server.models.address_tags import AddressTags
from openapi_server.models.neighbor_entities import NeighborEntities
from multidict import CIMultiDict
from openapi_server.models.search_result_level1 import SearchResultLevel1
from openapi_server.models.search_result_level2 import SearchResultLevel2
from openapi_server.models.search_result_level3 import SearchResultLevel3
from openapi_server.models.search_result_level4 import SearchResultLevel4
from openapi_server.models.search_result_level5 import SearchResultLevel5
from openapi_server.models.search_result_level6 import SearchResultLevel6
from openapi_server.models.search_result_leaf import SearchResultLeaf

import re
from gsrest.plugins import Plugin

from graphsenselib.tagstore.algorithms.obfuscate import (
    obfuscate_entity_actor,
    obfuscate_tag_if_not_public,
)

GROUPS_HEADER_NAME = "X-Consumer-Groups"
NO_OBFUSCATION_MARKER_GROUP = "private"
OBFUSCATION_MARKER_GROUP = "obfuscate"


class ObfuscateTags(Plugin):
    @classmethod
    def before_request(cls, context, request: web.Request):
        groups = [
            x.strip() for x in request.headers.get(GROUPS_HEADER_NAME, "").split(",")
        ]

        if NO_OBFUSCATION_MARKER_GROUP in groups:
            return request
        if "include_labels=true" in request.query_string.lower():
            return request
        if "/search" == request.path:
            return request
        if "/bulk" in request.path:
            return request
        if re.match(re.compile("/tags"), request.path):
            return request
        if re.match(re.compile("/[a-z]{3}/addresses/[^/]+$"), request.path):
            # to avoid loading actors for address
            return request

        # setting group for request.
        headers = dict(request.headers)
        headers[GROUPS_HEADER_NAME] = OBFUSCATION_MARKER_GROUP
        headers = CIMultiDict(**headers)
        return request.clone(headers=headers)

    @classmethod
    def before_response(cls, context, request: web.Request, result):
        # request.app.logger.debug(str(request.headers.get(GROUPS_HEADER_NAME, '')))
        groups = [
            x.strip() for x in request.headers.get(GROUPS_HEADER_NAME, "").split(",")
        ]

        if NO_OBFUSCATION_MARKER_GROUP in groups:
            return
        if isinstance(result, Entity):
            cls.obfuscate(result.best_address_tag)
            obfuscate_entity_actor(result)
            return
        if isinstance(result, AddressTags):
            cls.obfuscate(result.address_tags)
            return
        if isinstance(result, NeighborEntities):
            for neighbor in result.neighbors:
                cls.obfuscate(neighbor.entity.best_address_tag)
                obfuscate_entity_actor(neighbor.entity)
        if (
            isinstance(result, SearchResultLevel1)
            or isinstance(result, SearchResultLevel2)
            or isinstance(result, SearchResultLevel3)
            or isinstance(result, SearchResultLevel4)
            or isinstance(result, SearchResultLevel5)
            or isinstance(result, SearchResultLevel6)
            or isinstance(result, SearchResultLeaf)
        ):
            if result.neighbor:
                cls.obfuscate(result.neighbor.entity.best_address_tag)
            if not isinstance(result, SearchResultLeaf) and result.paths:
                for path in result.paths:
                    cls.before_response(context, request, path)
            return
        if isinstance(result, list):
            for r in result:
                cls.before_response(context, request, r)
            return

    @classmethod
    def obfuscate(cls, tags):
        if not tags:
            return
        if isinstance(tags, list):
            for tag in tags:
                obfuscate_tag_if_not_public(tag)
        else:
            obfuscate_tag_if_not_public(tags)
