from openapi_server.models.concept import Concept  # noqa: E501
from openapi_server.models.tag import Tag  # noqa: E501
from openapi_server.models.taxonomy import Taxonomy  # noqa: E501
import gsrest.service.tags_service as service
from gsrest.service.problems import notfound


def list_concepts(taxonomy):  # noqa: E501
    """Returns the supported concepts of a taxonomy

     # noqa: E501

    :param taxonomy: The taxonomy
    :type taxonomy: str

    :rtype: List[Concept]
    """
    try:
        return service.list_concepts(
            taxonomy=taxonomy)
    except RuntimeError as e:
        return notfound(str(e))


def list_tags(label, currency=None):  # noqa: E501
    """Returns the tags associated with a given label

     # noqa: E501

    :param label: The label of an entity
    :type label: str
    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str

    :rtype: List[Tag]
    """
    try:
        return service.list_tags(
            label=label,
            currency=currency)
    except RuntimeError as e:
        return notfound(str(e))


def list_taxonomies():  # noqa: E501
    """Returns the supported taxonomies

     # noqa: E501


    :rtype: List[Taxonomy]
    """
    try:
        return service.list_taxonomies(
            )
    except RuntimeError as e:
        return notfound(str(e))
