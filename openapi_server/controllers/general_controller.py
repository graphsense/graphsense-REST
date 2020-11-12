from openapi_server.models.stats import Stats  # noqa: E501
import gsrest.service.general_service as service
from gsrest.service.problems import notfound


def get_statistics():  # noqa: E501
    """Get statistics of supported currencies

     # noqa: E501


    :rtype: Stats
    """
    try:
        return service.get_statistics(
            )
    except RuntimeError as e:
        return notfound(str(e))
