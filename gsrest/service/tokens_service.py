from openapi_server.models.token_config import TokenConfig
from openapi_server.models.token_configs import TokenConfigs


async def list_supported_tokens(request, currency):
    db = request.app['db']
    if currency == "eth":
        return TokenConfigs([
            TokenConfig(ticker=k.lower(),
                        decimals=v["decimals"],
                        peg_currency=v["peg_currency"].lower())
            for k, v in db.get_token_configuration("eth").items()
        ])
    else:
        return TokenConfigs([])
