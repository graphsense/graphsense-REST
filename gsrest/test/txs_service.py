from openapi_server.models.txs import Txs
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.tx_utxo import TxUtxo
from openapi_server.models.tx_value import TxValue
from gsrest.util.values import make_values
import gsrest.service.txs_service as service

tx1 = TxUtxo(
   height=1,
   total_output=make_values(eur=0.0, usd=0.0, value=75137389),
   coinbase=False,
   outputs=[TxValue(
             address=["1HxbaBMF2jXBVnagoHvaA6rLxmaYL8gb8T"],
             value=make_values(eur=0.0, usd=0.0, value=75000000)),
            TxValue(
             address=["1MaFeRMwbk7AMk4fRd3xXpSiehoSqsvE5X"],
             value=make_values(eur=0.0, usd=0.0, value=137389))],
   inputs=[TxValue(
             address=["1MaFeRMwbk7AMk4fRd3xXpSiehoSqsvE5X"],
             value=make_values(eur=0.0, usd=0.0, value=75110000)),
           TxValue(
             address=["1MaFeRMwbk7AMk4fRd3xXpSiehoSqsvE5X"],
             value=make_values(eur=0.0, usd=0.0, value=37389))],
   timestamp=1434554207,
   total_input=make_values(eur=0.0, usd=0.0, value=75147389),
   tx_hash="ab1880"
)

tx2 = TxUtxo(
   timestamp=1373266967,
   total_output=make_values(eur=0.1, usd=0.2, value=9950000),
   coinbase=False,
   tx_hash="ab188013",
   total_input=make_values(eur=0.1, usd=0.2, value=10000000),
   outputs=[TxValue(
             address=["138cWsiAGpW9yqfjMVCCsFcnaiSHyoWMnJ"],
             value=make_values(eur=0.0, usd=0.0, value=1)),
            TxValue(
             address=["1CRqaDkksF1zp6wLunY7ygSafXsiftH9FN"],
             value=make_values(eur=0.1, usd=0.2, value=9949999))],
   inputs=[TxValue(
             address=["1H8omroLCN2578Mj6sDrWa8YueqWEckNKY"],
             value=make_values(eur=0.1, usd=0.2, value=10000000))],
   height=2)

tx3 = TxUtxo(
   timestamp=1373266967,
   total_output=make_values(eur=0.1, usd=0.2, value=9950000),
   coinbase=False,
   tx_hash="00ab188013",
   total_input=make_values(eur=0.1, usd=0.2, value=10000000),
   outputs=[TxValue(
             address=["138cWsiAGpW9yqfjMVCCsFcnaiSHyoWMnJ"],
             value=make_values(eur=0.0, usd=0.0, value=1)),
            TxValue(
             address=["1CRqaDkksF1zp6wLunY7ygSafXsiftH9FN"],
             value=make_values(eur=0.1, usd=0.2, value=9949999))],
   inputs=[TxValue(
             address=["1H8omroLCN2578Mj6sDrWa8YueqWEckNKY"],
             value=make_values(eur=0.1, usd=0.2, value=10000000))],
   height=2)

tx1_eth = TxAccount(
   tx_hash='af6e0000',
   height=1,
   timestamp=15,
   value=make_values(eur=123.0, usd=246.0, value=123000000000000000000))

tx2_eth = TxAccount(
   tx_hash='af6e0003',
   height=1,
   timestamp=16,
   value=make_values(eur=123.0, usd=246.0, value=123000000000000000000))

tx3_eth = TxAccount(
   tx_hash='ab188013',
   height=1,
   timestamp=17,
   value=make_values(eur=234.0, usd=468.0, value=234000000000000000000))

tx4_eth = TxAccount(
   tx_hash='123456',
   height=1,
   timestamp=17,
   value=make_values(eur=234.0, usd=468.0, value=234000000000000000000))


def get_tx(test_case):
    result = service.get_tx(currency='btc', tx_hash='ab1880')
    test_case.assertEqual(tx1, result)
    result = service.get_tx(currency='eth', tx_hash='af6e0000')
    test_case.assertEqual(tx1_eth, result)


def get_tx_io(test_case):
    result = service.get_tx_io(currency='btc', tx_hash='ab1880', io='inputs')
    test_case.assertEqual(tx1.inputs, result)
    result = service.get_tx_io(currency='btc', tx_hash='ab1880', io='outputs')
    test_case.assertEqual(tx1.outputs, result)


def list_txs(test_case):
    result = service.list_txs(currency='btc')
    result_hashes = [tx.tx_hash for tx in result.txs]
    tx_hashes = [
            'abcdef',
            '4567',
            '123456',
            'ab1880',
            'ab188013',
            '00ab188013',
            '04d92601677d62a985310b61a301e74870fa942c8be0648e16b1db23b996a8cd',
            'bd01b57a50bdee0fb34ce77f5c62a664cea5b94b304d438a8225850f05b45ae5',
            '6e7456a7a0e4cc2c4ade617e4e950ece015c00add338be345ce2b544e5a86322',
            '4567',
            '5678',
            '123456']

    test_case.assertEqual(tx_hashes, result_hashes)
    result = service.list_txs(currency='eth')
    txs = sorted([tx1_eth, tx2_eth, tx3_eth, tx4_eth],
                 key=lambda tx: tx.tx_hash)
    result.txs = sorted(result.txs, key=lambda tx: tx.tx_hash)
    test_case.assertEqual(Txs(next_page=None,
                              txs=txs),
                          result)
