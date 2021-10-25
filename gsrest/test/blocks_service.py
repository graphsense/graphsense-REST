from openapi_server.models.block import Block
from openapi_server.models.tx_utxo import TxUtxo
from openapi_server.models.tx_account import TxAccount
from gsrest.test.txs_service import tx1, tx1_eth, tx2_eth

block = Block(
        height=1,
        block_hash="00000000839a8e6886ab5951d76f"
        "411475428afc90947ee320161bbf18eb6048",
        no_txs=1,
        timestamp=1231469665)

block2 = Block(
        height=2,
        block_hash="000000006a625f06636b8bb6ac7b9"
        "60a8d03705d1ace08b1a19da3fdcc99ddbd",
        no_txs=1,
        timestamp=1231469744)

eth_block = Block(
        height=1,
        block_hash="123456",
        no_txs=5,
        timestamp=123)

eth_block2 = Block(
        height=2300001,
        block_hash="234567",
        no_txs=0,
        timestamp=234)


async def get_block(test_case):
    """Test case for get_block
    """
    path = '/{currency}/blocks/{height}'
    result = await test_case.request(path, currency="btc", height=1)
    test_case.assertEqual(block, Block.from_dict(result))
    result = await test_case.request(path, currency="btc", height=2)
    test_case.assertEqual(block2, Block.from_dict(result))

    result = await test_case.request(path, currency="eth", height=1)
    test_case.assertEqual(eth_block, Block.from_dict(result))
    result = await test_case.request(path, currency="eth", height=2300001)
    test_case.assertEqual(eth_block2, Block.from_dict(result))

    await test_case.requestWithCode(path, 404,
                                    currency="btc", height="0")

    await test_case.requestWithCode(path, 404,
                                    currency="eth", height="0")


async def list_block_txs(test_case):
    """Test case for list_block_txs
    """

    path = '/{currency}/blocks/{height}/txs'
    block_txs = [tx1]
    result = await test_case.request(path, currency="btc", height=1)
    test_case.assertEqual(block_txs, [TxUtxo.from_dict(r) for r in result])

    result = await test_case.request(path, currency="eth", height=1)

    result = [TxAccount.from_dict(r) for r in result]

    def s(tx):
        return tx.tx_hash

    result = sorted(result, key=s)
    test_case.assertEqual(
        sorted([tx1_eth, tx2_eth], key=s),
        result)
