from openapi_server.models.block import Block
from openapi_server.models.blocks import Blocks
import gsrest.service.blocks_service as service
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

    result = await service.get_block("btc", 1)
    test_case.assertEqual(block, result)
    result = await service.get_block("btc", 2)
    test_case.assertEqual(block2, result)

    result = await service.get_block("eth", 1)
    test_case.assertEqual(eth_block, result)
    result = await service.get_block("eth", 2300001)
    test_case.assertEqual(eth_block2, result)


def get_block_sync(test_case):
    headers = {
        'Accept': 'application/json',
    }
    response = test_case.client.open(
        '/{currency}/blocks/{height}'.format(currency="btc", height="0"),
        method='GET',
        headers=headers)
    test_case.assert404(response,
                        'Response body is : ' + response.data.decode('utf-8'))

    headers = {
        'Accept': 'application/json',
    }
    response = test_case.client.open(
        '/eth/blocks/{height}'.format(height="0"),
        method='GET',
        headers=headers)
    test_case.assert404(response,
                        'Response body is : ' + response.data.decode('utf-8'))

async def list_block_txs(test_case):
    """Test case for list_block_txs
    """

    block_txs = [tx1]
    result = await service.list_block_txs("btc", 1)
    test_case.assertEqual(block_txs, result)

    result = await service.list_block_txs("eth", 1)

    def s(tx):
        return tx.tx_hash

    result = sorted(result, key=s)
    test_case.assertEqual(
        sorted([tx1_eth, tx2_eth], key=s),
        result)


def list_block_txs_csv(test_case):
    """Test case for list_block_txs_csv
    """
    result = service.list_block_txs_csv("btc", 2).data.decode('utf-8')
    splitted = result.split("\r\n")
    test_case.assertEqual(3, len(splitted))
    test_case.assertEqual(13, len(splitted[0].split(',')))

    result = service.list_block_txs_csv("eth", 1).data.decode('utf-8')
    splitted = result.split("\r\n")
    test_case.assertEqual(4, len(splitted))
    test_case.assertEqual(7, len(splitted[0].split(',')))


async def list_blocks(test_case):
    """Test case for list_blocks
    """
    blocks = Blocks(next_page=None, blocks=[block, block2])
    result = await service.list_blocks("btc")
    result = Blocks(
            next_page=None,
            blocks=sorted(result.blocks,
                          key=lambda block: block.height))
    test_case.assertEqual(blocks, result)

    blocks = Blocks(next_page=None, blocks=[eth_block, eth_block2])
    result = await service.list_blocks("eth")
    result = Blocks(
            next_page=None,
            blocks=sorted(result.blocks,
                          key=lambda block: block.height))
    test_case.assertEqual(blocks, result)
