from openapi_server.models.token_config import TokenConfig
from openapi_server.models.token_configs import TokenConfigs
from gsrest.util import is_eth_like

async def list_supported_tokens(request, currency):
    db = request.app['db']
    if is_eth_like(currency):
        return TokenConfigs([
            TokenConfig(ticker=k.lower(),
                        decimals=v["decimals"],
                        peg_currency=v["peg_currency"].lower())
            for k, v in db.get_token_configuration(currency).items()
        ])
    else:
        return TokenConfigs([])
