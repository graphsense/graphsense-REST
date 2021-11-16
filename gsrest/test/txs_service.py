from openapi_server.models.tx_account import TxAccount
from openapi_server.models.tx_utxo import TxUtxo
from openapi_server.models.tx_value import TxValue
from gsrest.util.values import make_values

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
   from_address='0xbe370541310b13922e209515ebffe8d459e050',
   to_address='0xd6cc43ac66902302074a19e52bacc68d15421551',
   value=make_values(eur=123.0, usd=246.0, value=123000000000000000000))

tx2_eth = TxAccount(
   tx_hash='af6e0003',
   height=1,
   timestamp=16,
   from_address='0xea674fdde714fd979de3edf0f56aa9716b898ec8',
   to_address='0xe0ec83c0c2bcffd920d268b20f403652e7137dbe',
   value=make_values(eur=123.0, usd=246.0, value=123000000000000000000))

tx22_eth = TxAccount(
   tx_hash='af6e0004',
   height=1,
   timestamp=16,
   from_address='0xea674fdde714fd979de3edf0f56aa9716b898ec8',
   to_address='0xe0ec83c0c2bcffd920d268b20f403652e7137dbe',
   value=make_values(eur=124.0, usd=248.0, value=124000000000000000000))

tx3_eth = TxAccount(
   tx_hash='ab188013',
   height=1,
   timestamp=17,
   from_address='0xea674fdde714fd979de3edf0f56aa9716b898ec8',
   to_address='0xe0ec83c0c2bcffd920d268b20f403652e7137dbe',
   value=make_values(eur=234.0, usd=468.0, value=234000000000000000000))

tx4_eth = TxAccount(
   tx_hash='123456',
   height=1,
   timestamp=17,
   from_address='0xea674fdde714fd979de3edf0f56aa9716b898ec8',
   to_address='0xe0ec83c0c2bcffd920d268b20f403652e7137dbe',
   value=make_values(eur=234.0, usd=468.0, value=234000000000000000000))


async def get_tx(test_case):
    path = '/{currency}/txs/{tx_hash}?include_io={include_io}'
    result = await test_case.request(path,
                                     currency='btc',
                                     tx_hash='ab1880',
                                     include_io=True)
    test_case.assertEqual(tx1.to_dict(), result)
    result = await test_case.request(path,
                                     currency='btc',
                                     tx_hash='ab1880',
                                     include_io=False)
    tx = tx1.to_dict()
    tx.pop('inputs')
    tx.pop('outputs')
    test_case.assertEqual(tx, result)
    result = await test_case.request(path,
                                     currency='eth',
                                     tx_hash='af6e0000',
                                     include_io=True)
    test_case.assertEqual(tx1_eth.to_dict(), result)


async def get_tx_io(test_case):
    path = '/{currency}/txs/{tx_hash}/{io}'
    result = await test_case.request(path,
                                     currency='btc',
                                     tx_hash='ab1880',
                                     io='inputs')

    test_case.assertEqual(tx1.to_dict()['inputs'], result)
    result = await test_case.request(path,
                                     currency='btc',
                                     tx_hash='ab1880',
                                     io='outputs')
    test_case.assertEqual(tx1.to_dict()['outputs'], result)
