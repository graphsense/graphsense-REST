from openapi_server.models.token_configs import TokenConfigs
from openapi_server.models.token_config import TokenConfig

btc_tokens = TokenConfigs([])
eth_tokens = TokenConfigs([
    TokenConfig(ticker="usdc", decimals=6, peg_currency="usd"),
    TokenConfig(ticker="weth", decimals=18, peg_currency="eth"),
    TokenConfig(ticker="usdt", decimals=6, peg_currency="usd"),
])


async def list_supported_tokens(test_case):
    """Test case for list_supported_tokens
    """
    path = '/{currency}/supported_tokens/'
    result = await test_case.request(path, currency="btc")

    assert result == btc_tokens.to_dict()

    path = '/{currency}/supported_tokens/'
    result = await test_case.request(path, currency="eth")

    assert result == eth_tokens.to_dict()
