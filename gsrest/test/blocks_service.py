from openapi_server.models.block import Block
from openapi_server.models.blocks import Blocks
from openapi_server.models.block_txs import BlockTxs
from openapi_server.models.block_tx_summary import BlockTxSummary
from openapi_server.models.values import Values
import gsrest.service.blocks_service as service
from gsrest.test.assertion import assertEqual

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


def get_block(test_case):
    """Test case for get_block
    """

    result = service.get_block("btc", 1)
    assertEqual(block, result)
    result = service.get_block("btc", 2)
    assertEqual(block2, result)
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
    assertEqual(block_txs, result)


def list_block_txs_csv(test_case):
    """Test case for list_block_txs_csv
    """
    csv = ("block_height,no_inputs,no_outputs,total_input_eur,"
           "total_input_usd,total_input_value,total_output_eur,"
           "total_output_usd,total_output_value,tx_hash\n1,0,1,0.0"
           ",0.0,0,0.0,0.0,5000000000,0e3e2357e806b6cdb1f70b54c3a3a17b"
           "6714ee1f0e68bebb44a74b1efd512098\n")
    assertEqual(csv, service.list_block_txs_csv("btc", 1).data.decode('utf-8'))


def list_blocks(test_case):
    """Test case for list_blocks
    """
    blocks = Blocks(next_page=None, blocks=[block, block2])
    result = service.list_blocks("btc")
    result = Blocks(
            next_page=None,
            blocks=sorted(result.blocks,
                          key=lambda block: block.height))
    assertEqual(blocks, result)
