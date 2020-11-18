from openapi_server.models.tx import Tx
from openapi_server.models.txs import Txs
from openapi_server.models.tx_value import TxValue
from openapi_server.models.values import Values
from gsrest.test.assertion import assertEqual
import gsrest.service.txs_service as service

tx1 = Tx(
   height=1,
   total_output=Values(eur=0.0, usd=0.0, value=75137389),
   coinbase=False,
   outputs=[TxValue(
             address=["1HxbaBMF2jXBVnagoHvaA6rLxmaYL8gb8T"],
             value=Values(eur=0.0, usd=0.0, value=75000000)),
            TxValue(
             address=["1MaFeRMwbk7AMk4fRd3xXpSiehoSqsvE5X"],
             value=Values(eur=0.0, usd=0.0, value=137389))],
   inputs=[TxValue(
             address=["1MaFeRMwbk7AMk4fRd3xXpSiehoSqsvE5X"],
             value=Values(eur=0.0, usd=0.0, value=75110000)),
           TxValue(
             address=["1MaFeRMwbk7AMk4fRd3xXpSiehoSqsvE5X"],
             value=Values(eur=0.0, usd=0.0, value=37389))],
   timestamp=1434554207,
   total_input=Values(eur=0.0, usd=0.0, value=75147389),
   tx_hash="ab1880"
)

tx2 = Tx(
   timestamp=1373266967,
   total_output=Values(eur=0.1, usd=0.2, value=9950000),
   coinbase=False,
   tx_hash="ab188013",
   total_input=Values(eur=0.1, usd=0.2, value=10000000),
   outputs=[TxValue(
             address=["138cWsiAGpW9yqfjMVCCsFcnaiSHyoWMnJ"],
             value=Values(eur=0.0, usd=0.0, value=1)),
            TxValue(
             address=["1CRqaDkksF1zp6wLunY7ygSafXsiftH9FN"],
             value=Values(eur=0.1, usd=0.2, value=9949999))],
   inputs=[TxValue(
             address=["1H8omroLCN2578Mj6sDrWa8YueqWEckNKY"],
             value=Values(eur=0.1, usd=0.2, value=10000000))],
   height=2)

tx3 = Tx(
   timestamp=1373266967,
   total_output=Values(eur=0.1, usd=0.2, value=9950000),
   coinbase=False,
   tx_hash="00ab188013",
   total_input=Values(eur=0.1, usd=0.2, value=10000000),
   outputs=[TxValue(
             address=["138cWsiAGpW9yqfjMVCCsFcnaiSHyoWMnJ"],
             value=Values(eur=0.0, usd=0.0, value=1)),
            TxValue(
             address=["1CRqaDkksF1zp6wLunY7ygSafXsiftH9FN"],
             value=Values(eur=0.1, usd=0.2, value=9949999))],
   inputs=[TxValue(
             address=["1H8omroLCN2578Mj6sDrWa8YueqWEckNKY"],
             value=Values(eur=0.1, usd=0.2, value=10000000))],
   height=2)


def get_tx(test_case):
    result = service.get_tx(currency='btc', tx_hash='ab1880')
    assertEqual(tx1, result)


def list_txs(test_case):
    result = service.list_txs(currency='btc')
    assertEqual(Txs(next_page=None, txs=[tx1, tx2, tx3]), result)
