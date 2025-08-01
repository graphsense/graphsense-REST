from gsrest.util import is_eth_like
from openapi_server.models.rate import Rate
from openapi_server.models.values import Values


def make_values(value, eur, usd):
    return Values(
        value=value,
        fiat_values=[Rate("eur", round(eur, 2)), Rate("usd", round(usd, 2))],
    )


def catchNaN(v):
    if v != v:
        return None
    return v


def map_rates_for_peged_tokens(rates, token_config):
    peg = token_config["peg_currency"].lower()
    if peg == "usd":
        if len(rates) != 2:
            raise Exception(
                f"Rates structure is expected to be a list of length 2: {rates}"
            )
        r = {i["code"]: i["value"] for i in rates}

        return [
            {"code": "eur", "value": r["eur"] / r["usd"]},
            {"code": "usd", "value": 1},
        ]
    elif peg == "eur":
        if len(rates) != 2:
            raise Exception(
                f"Rates structure is expected to be a list of length 2: {rates}"
            )
        r = {i["code"]: i["value"] for i in rates}

        return [
            {"code": "eur", "value": 1},
            {"code": "usd", "value": r["usd"] / r["eur"]},
        ]

    elif is_eth_like(peg):
        return rates
    else:
        raise Exception(
            "Currently only tokens pegged to ether, euro or usd are supported"
        )


def convert_token_values_map(currency, value_map, rates, token_configs):
    if value_map is None:
        return None
    else:
        return {
            token_currency.lower(): convert_token_value(
                value, rates, token_configs[token_currency]
            )
            for token_currency, value in value_map.items()
        }


def convert_value_impl(value, rates, factor):
    return Values(
        value=catchNaN(value),
        fiat_values=[
            Rate(r["code"], catchNaN(round(value * r["value"] * factor, 2)))
            for r in rates
        ],
    )


def convert_token_value(value, rates, token_config):
    return convert_value_impl(
        value,
        map_rates_for_peged_tokens(rates, token_config),
        1 / token_config["decimal_divisor"],
    )


def convert_value(currency, value, rates):
    if currency == "eth":
        factor = 1e-18
    elif currency == "trx":
        factor = 1e-6
    else:
        factor = 1e-8

    return convert_value_impl(value, rates, factor)


def to_values_tokens(token_values):
    if token_values is None:
        return None
    return {k.lower(): to_values(value) for k, value in token_values.items()}


def to_values(value):
    return Values(
        value=catchNaN(value.value),
        fiat_values=[
            Rate(r["code"], catchNaN(round(r["value"], 2))) for r in value.fiat_values
        ],
    )
