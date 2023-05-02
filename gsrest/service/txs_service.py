from openapi_server.models.tx_utxo import TxUtxo
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.tx_value import TxValue
from gsrest.service.rates_service import get_rates
from gsrest.util.values import convert_value, convert_token_value


def from_row(currency, row, rates, token_config, include_io=False):
    if currency == 'eth':
        return TxAccount(
            currency=currency
            if "token_tx_id" not in row else row["currency"].lower(),
            tx_hash=row['tx_hash'].hex(),
            timestamp=row['block_timestamp'],
            height=row['block_id'],
            from_address=row['from_address'],
            to_address=row['to_address'],
            token_tx_id=row.get("token_tx_id", None),
            contract_creation=row.get("contract_creation", None),
            value=convert_value(currency, row['value'], rates)
            if "token_tx_id" not in row else convert_token_value(
                row['value'], rates, token_config[row["currency"]]))

    return TxUtxo(currency=currency,
                  tx_hash=row['tx_hash'].hex(),
                  coinbase=row['coinbase'],
                  height=row['block_id'],
                  no_inputs=0 if not row['inputs'] else len(row['inputs']),
                  no_outputs=0 if not row['outputs'] else len(row['outputs']),
                  inputs=io_from_rows(currency, row, 'inputs', rates,
                                      include_io),
                  outputs=io_from_rows(currency, row, 'outputs', rates,
                                       include_io),
                  timestamp=row['timestamp'],
                  total_input=convert_value(currency, row['total_input'],
                                            rates),
                  total_output=convert_value(currency, row['total_output'],
                                             rates))


def io_from_rows(currency, values, key, rates, include_io):
    if not include_io:
        return None
    if key not in values:
        return None
    if not values[key]:
        return []
    return [
        TxValue(address=i.address,
                value=convert_value(currency, i.value, rates))
        for i in values[key] if i.address is not None
    ]


async def list_token_txs(request, currency, tx_hash, token_tx_id=None):
    db = request.app['db']
    results = await db.list_token_txs(currency, tx_hash, log_index=token_tx_id)
    if results is None:
        raise RuntimeError('Transaction {} in keyspace {} not found'.format(
            tx_hash, currency))

    results = [
        from_row(currency, result, (await
                                    get_rates(request, currency,
                                              result['block_id']))['rates'],
                 db.get_token_configuration(currency)) for result in results
    ]

    return results


async def get_tx(request,
                 currency,
                 tx_hash,
                 token_tx_id=None,
                 include_io=False):
    db = request.app['db']

    if token_tx_id is not None:
        if currency == 'eth':
            results = await list_token_txs(request,
                                           currency,
                                           tx_hash,
                                           token_tx_id=token_tx_id)

            if len(results):
                return results[0]
            else:
                raise RuntimeError(
                    'Token transaction {}:{} in keyspace {} not found'.format(
                        tx_hash, token_tx_id, currency))
        else:
            raise RuntimeError(
                f'{currency} does not support token transactions.')
    else:
        result = await db.get_tx(currency, tx_hash)
        if result is None:
            raise RuntimeError(
                'Transaction {} in keyspace {} not found'.format(
                    tx_hash, currency))

        rates = (await get_rates(request, currency,
                                 result['block_id']))['rates']

        result = from_row(currency, result, rates,
                          db.get_token_configuration(currency), include_io)
        return result


async def get_tx_io(request, currency, tx_hash, io):
    if currency == 'eth':
        raise RuntimeError('get_tx_io not implemented for ETH')
    result = await get_tx(request, currency, tx_hash, include_io=True)
    return getattr(result, io)


async def list_matching_txs(request, currency, expression):
    db = request.app['db']
    results = await db.list_matching_txs(currency, expression)

    leading_zeros = 0
    pos = 0
    # leading zeros will be lost when casting to int
    while expression[pos] == "0":
        pos += 1
        leading_zeros += 1

    txs = [
        "0" * leading_zeros +
        str(hex(int.from_bytes(row['tx_hash'], byteorder="big")))[2:]
        for row in results
    ]
    return [tx for tx in txs if tx.startswith(expression)]
