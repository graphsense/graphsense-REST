import connexion
import six
import traceback
import asyncio

from openapi_server.models.concept import Concept  # noqa: E501
from openapi_server.models.tags import Tags  # noqa: E501
from openapi_server.models.taxonomy import Taxonomy  # noqa: E501
import gsrest.service.tags_service as service
from gsrest.service.problems import notfound, badrequest, internalerror


def list_concepts(taxonomy):  # noqa: E501
    """Returns the supported concepts of a taxonomy

     # noqa: E501

    :param taxonomy: The taxonomy
    :type taxonomy: str

    :rtype: List[Concept]
    """
    try:
        result = asyncio.run(
            service.list_concepts(
                taxonomy=taxonomy))
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except TypeError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")


def list_tags(label, currency=None):  # noqa: E501
    """Returns address and entity tags associated with a given label

     # noqa: E501

    :param label: The label of an entity
    :type label: str
    :param currency: The cryptocurrency (e.g., btc)
    :type currency: str

    :rtype: List[Tags]
    """
    try:
        result = asyncio.run(
            service.list_tags(
                label=label,
                currency=currency))
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except TypeError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")


def list_taxonomies():  # noqa: E501
    """Returns the supported taxonomies

     # noqa: E501


    :rtype: List[Taxonomy]
    """
    try:
        result = asyncio.run(
            service.list_taxonomies(
                ))
        return result
    except RuntimeError as e:
        return notfound(str(e))
    except ValueError as e:
        return badrequest(str(e))
    except TypeError as e:
        return badrequest(str(e))
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return internalerror("")
