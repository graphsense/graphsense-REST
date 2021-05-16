from openapi_server.models.block import Block
from openapi_server.models.block_eth import BlockEth
from openapi_server.models.blocks import Blocks
from openapi_server.models.blocks_eth import BlocksEth
from openapi_server.models.block_txs import BlockTxs
from openapi_server.models.txs import Txs
from openapi_server.models.tx_account import TxAccount
from openapi_server.models.block_tx_summary import BlockTxSummary
from openapi_server.models.values import Values
import gsrest.service.blocks_service as service

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

eth_block = BlockEth(
        height=1,
        block_hash="123456",
        no_txs=5,
        timestamp=123)

eth_block2 = BlockEth(
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


def list_block_txs(test_case):
    """Test case for list_block_txs
    """

    block_txs = BlockTxs(height=1, txs=[
            BlockTxSummary(
                no_inputs=0,
                no_outputs=1,
                total_input=Values(eur=0, usd=0, value=0),
                total_output=Values(eur=0, usd=0, value=5000000000),
                tx_hash="0e3e2357e806b6cdb1f70b54c3a3"
                "a17b6714ee1f0e68bebb44a74b1efd512098"
                )
            ])
    result = service.list_block_txs("btc", 1)
    test_case.assertEqual(block_txs, result)


def list_block_txs_csv(test_case):
    """Test case for list_block_txs_csv
    """
    csv = ("block_height,no_inputs,no_outputs,total_input_eur,"
           "total_input_usd,total_input_value,total_output_eur,"
           "total_output_usd,total_output_value,tx_hash\r\n1,0,1,0.0"
           ",0.0,0,0.0,0.0,5000000000,0e3e2357e806b6cdb1f70b54c3a3a17b"
           "6714ee1f0e68bebb44a74b1efd512098\r\n")
    test_case.assertEqual(csv,
                          service.list_block_txs_csv("btc", 1)
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


def get_block_eth(test_case):
    """Test case for get_block_eth
    """

    result = service.get_block_eth(1)
    test_case.assertEqual(eth_block, result)
    result = service.get_block_eth(2300001)
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


def list_blocks_eth(test_case):
    """Test case for list_blocks_eth
    """
    blocks = BlocksEth(next_page=None, blocks=[eth_block, eth_block2])
    result = service.list_blocks_eth()
    result = BlocksEth(
            next_page=None,
            blocks=sorted(result.blocks,
                          key=lambda block: block.height))
    test_case.assertEqual(blocks, result)


def list_block_txs_eth(test_case):
    """Test case for list_block_txs_eth
    """

    block_txs = Txs(txs=[
            TxAccount(
                tx_hash='af6e0000',
                height=1,
                timestamp=15,
                values=Values(eur=123.0, usd=246.0, value=12300000000)),
            TxAccount(
                tx_hash='af6e0003',
                height=1,
                timestamp=16,
                values=Values(eur=234.0, usd=468.0, value=23400000000))
            ])
    result = service.list_block_txs_eth(1)
    test_case.assertEqual(block_txs, result)


def list_block_txs_csv_eth(test_case):
    """Test case for list_block_txs_csv_eth
    """
    csv = ("height,timestamp,tx_hash,values_eur,values_usd,values_value\r\n"
           "1,15,af6e0000,123.0,246.0,12300000000\r\n"
           "1,16,af6e0003,234.0,468.0,23400000000\r\n")
    test_case.assertEqual(csv,
                          service.list_block_txs_csv_eth(1)
                          .data.decode('utf-8'))
