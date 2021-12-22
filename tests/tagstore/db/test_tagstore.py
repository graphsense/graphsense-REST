import asyncio
from tests import BaseTestCase
import pprint
from gsrest.db.util import encode_page_handles, decode_page_handles


class TestTagstore(BaseTestCase):

    def test_page_handles(test_case):
        pagesAndIds = [(1, "ts1"),
                       (5, "ts2"),
                       (100000, "ts3")]
        composed = encode_page_handles(pagesAndIds)

        print(f'composed {composed}')

        test_case.assertEqual(composed,
                              "dHMxfE1RPT0kdHMyfE5RPT0kdHMzfE1UQXdNREF3")

        decomposed = decode_page_handles(composed)

        dic = {}
        for (page, id) in pagesAndIds:
            dic[id] = str(page)

        test_case.assertEqual(decomposed, dic)

    def test_empty_page_handles(test_case):
        composed = encode_page_handles([])

        test_case.assertIsNone(composed)

        decomposed = decode_page_handles(composed)

        test_case.assertEqual(decomposed, {})

        decomposed = decode_page_handles("")

        test_case.assertEqual(decomposed, {})

    def test_partly_empty_page_handles(test_case):
        pagesAndIds = [(None, "ts1"),
                       ("xyz", "ts2")]

        composed = encode_page_handles(pagesAndIds)

        print(f'composed {composed}')

        test_case.assertEqual(composed,
                              "dHMyfGVIbDY=")

        decomposed = decode_page_handles(composed)

        dic = {}
        for (page, id) in pagesAndIds:
            if page is None:
                continue
            dic[id] = str(page)

        test_case.assertEqual(decomposed, dic)

