from typing import Any

from tagstore.db import TagstoreDbAsync, Taxonomies

from gsrest.config import GSRestConfig
from gsrest.services.addresses_service import AddressesService
from gsrest.services.blocks_service import BlocksService
from gsrest.services.conversions_service import ConversionsService
from gsrest.services.entities_service import EntitiesService
from gsrest.services.general_service import GeneralService
from gsrest.services.rates_service import RatesService
from gsrest.services.stats_service import StatsService
from gsrest.services.tags_service import ConceptProtocol, TagsService
from gsrest.services.tokens_service import TokensService
from gsrest.services.txs_service import TxsService


class ConceptsCacheService(ConceptProtocol):
    def __init__(self, app: Any, logger: Any):
        self.logger = logger
        self.app = app

    def get_is_abuse(self, concept: str) -> bool:
        return concept in self.app["taxonomy-cache"]["abuse"]

    def get_taxonomy_concept_label(self, taxonomy: Any, concept_id: str) -> str:
        return self.app["taxonomy-cache"]["labels"][taxonomy].get(concept_id, None)

    @classmethod
    async def setup_cache(cls, db_engine: Any, app: Any):
        tagstore_db = TagstoreDbAsync(db_engine)
        taxs = await tagstore_db.get_taxonomies(
            {Taxonomies.CONCEPT, Taxonomies.COUNTRY}
        )
        app["taxonomy-cache"] = {
            "labels": {
                Taxonomies.CONCEPT: {x.id: x.label for x in taxs.concept},
                Taxonomies.COUNTRY: {x.id: x.label for x in taxs.country},
            },
            "abuse": {x.id for x in taxs.concept if x.is_abuse},
        }


class ServiceContainer:
    def __init__(
        self,
        config: GSRestConfig,
        db: any,
        tagstore_engine: any,
        concepts_cache_service: ConceptsCacheService,
        logger: any,
    ):
        self.config = config
        self.db = db
        self.tagstore_db = TagstoreDbAsync(tagstore_engine)
        self.logger = logger
        self.category_cache_service = concepts_cache_service

        # Initialize services with dependencies
        self._rates_service = RatesService(db=db, logger=logger)
        self._tokens_service = TokensService(db=db, logger=logger)
        self._stats_service = StatsService(
            db=db, tagstore=self.tagstore_db, logger=logger
        )

        self._tags_service = TagsService(
            tagstore=self.tagstore_db,
            concepts_cache_service=self.category_cache_service,
            logger=logger,
        )
        self._txs_service = TxsService(
            db=db, rates_service=self._rates_service, logger=logger
        )
        self._blocks_service = BlocksService(
            db=db,
            rates_service=self._rates_service,
            config=config,
            logger=logger,
        )
        self._general_service = GeneralService(
            db=db,
            tagstore=self.tagstore_db,
            stats_service=self._stats_service,
            logger=logger,
        )
        self._conversions_service = ConversionsService(logger=logger)
        self._addresses_service = AddressesService(
            db=db,
            tagstore=self.tagstore_db,
            tags_service=self._tags_service,
            entities_service=None,  # Will be set later to avoid circular dependency
            blocks_service=self._blocks_service,
            rates_service=self._rates_service,
            logger=logger,
        )
        self._entities_service = EntitiesService(
            db=db,
            tagstore=self.tagstore_db,
            tags_service=self._tags_service,
            blocks_service=self._blocks_service,
            rates_service=self._rates_service,
            logger=logger,
        )

        # Set up circular dependency
        self._rates_service.set_stats_service(self._stats_service)

        # Set circular dependency for addresses service
        self._addresses_service.entities_service = self._entities_service

    @property
    def tags_service(self) -> TagsService:
        return self._tags_service

    @property
    def rates_service(self) -> RatesService:
        return self._rates_service

    @property
    def blocks_service(self) -> BlocksService:
        return self._blocks_service

    @property
    def tokens_service(self) -> TokensService:
        return self._tokens_service

    @property
    def stats_service(self) -> StatsService:
        return self._stats_service

    @property
    def txs_service(self) -> TxsService:
        return self._txs_service

    @property
    def general_service(self) -> GeneralService:
        return self._general_service

    @property
    def conversions_service(self) -> ConversionsService:
        return self._conversions_service

    @property
    def addresses_service(self) -> AddressesService:
        return self._addresses_service

    @property
    def entities_service(self) -> EntitiesService:
        return self._entities_service

    @property
    def cache_service(self) -> ConceptProtocol:
        return self._cache_service


def get_service_container(request) -> ServiceContainer:
    """Extract service container from request"""
    return request.app["services"]


def get_request_cache(request):
    if not hasattr(request, "_cache"):
        request._cache = {}
    return request._cache


def get_user_tags_acl_group(request) -> str:
    return request.app["config"].user_tag_reporting_acl_group


def get_tagstore_access_groups(request):
    return (
        ["public"]
        if not request.app["request_config"]["show_private_tags"]
        else ["public", "private"]
    ) + [get_user_tags_acl_group(request)]
