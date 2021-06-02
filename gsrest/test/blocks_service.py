from openapi_server.models.block import Block
from openapi_server.models.blocks import Blocks
from openapi_server.models.block_tx_utxo import BlockTxUtxo
from openapi_server.models.values import Values
import gsrest.service.blocks_service as service
from gsrest.test.txs_service import tx1_eth, tx2_eth

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


def get_block(test_case):
    """Test case for get_block
    """

    result = service.get_block("btc", 1)
    test_case.assertEqual(block, result)
    result = service.get_block("btc", 2)
    test_case.assertEqual(block2, result)
    headers = {
        'Accept': 'application/json',
    }
    response = test_case.client.open(
        '/{currency}/blocks/{height}'.format(currency="btc", height="0"),
        method='GET',
        headers=headers)
    test_case.assert400(response,
                        'Response body is : ' + response.data.decode('utf-8'))

    result = service.get_block("eth", 1)
    test_case.assertEqual(eth_block, result)
    result = service.get_block("eth", 2300001)
    test_case.assertEqual(eth_block2, result)
    headers = {
        'Accept': 'application/json',
    }
    response = test_case.client.open(
        '/eth/blocks/{height}'.format(height="0"),
        method='GET',
        headers=headers)
    test_case.assert400(response,
                        'Response body is : ' + response.data.decode('utf-8'))


def list_block_txs(test_case):
    """Test case for list_block_txs
    """

    block_txs = [
            BlockTxUtxo(
                no_inputs=0,
                no_outputs=1,
                total_input=Values(eur=0.0, usd=0.0, value=0),
                total_output=Values(eur=0.0, usd=0.0, value=5000000000),
                tx_hash="ab1880"
                )
            ]
    result = service.list_block_txs("btc", 1)
    test_case.assertEqual(block_txs, result)

    result = service.list_block_txs("eth", 1)
    test_case.assertEqual([tx1_eth, tx2_eth], result)


def list_block_txs_csv(test_case):
    """Test case for list_block_txs_csv
    """
    csv = ("currency_type,no_inputs,no_outputs,total_input_eur,"
           "total_input_usd,total_input_value,total_output_eur,"
           "total_output_usd,total_output_value,tx_hash\r\nutxo,0,1,0.0"
           ",0.0,0,0.0,0.0,5000000000,ab1880\r\n")
    test_case.assertEqual(csv,
                          service.list_block_txs_csv("btc", 1)
                          .data.decode('utf-8'))

    csv = ("currency_type,height,timestamp,tx_hash,values_eur,"
           "values_usd,values_value\r\n"
           "account,1,15,af6e0000,123.0,246.0,123000000000000000000\r\n"
           "account,1,16,af6e0003,234.0,468.0,234000000000000000000\r\n")
    test_case.assertEqual(csv,
                          service.list_block_txs_csv("eth", 1)
                          .data.decode('utf-8'))


def list_blocks(test_case):
    """Test case for list_blocks
    """
    blocks = Blocks(next_page=None, blocks=[block, block2])
    result = service.list_blocks("btc")
    result = Blocks(
            next_page=None,
            blocks=sorted(result.blocks,
                          key=lambda block: block.height))
    test_case.assertEqual(blocks, result)

    blocks = Blocks(next_page=None, blocks=[eth_block, eth_block2])
    result = service.list_blocks("eth")
    result = Blocks(
            next_page=None,
            blocks=sorted(result.blocks,
                          key=lambda block: block.height))
    test_case.assertEqual(blocks, result)
