from gsrest.db import get_connection
import asyncio
from openapi_server.test import BaseTestCase
import pprint


class TestCassandra(BaseTestCase):

    def test_concurrent_with_args(test_case):
        db = get_connection()

        query = "select tx_id from transaction where tx_id_group = %s"
        params = [[0], [1]]
        result = asyncio.run(db.concurrent_with_args("btc", "raw", query,
                                                     params, one=False))
        pprint.pprint(result)
        txs = [[{'tx_id': 345},
                {'tx_id': 456},
                {'tx_id': 567},
                {'tx_id': 4567},
                {'tx_id': 5678}],
               [{'tx_id': 25001},
                {'tx_id': 25002},
                {'tx_id': 25003}]]

        result = asyncio.run(db.execute_async("btc", "raw", query,
                                              params[0], autopaging=True,
                                              fetch_size=1))
        test_case.assertEqual(txs[0], result.current_rows)
