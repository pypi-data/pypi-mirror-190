from unittest import TestCase
from .. import AdressApi, SearchResponse, ReverseResponse

import time
import requests
WAIT_TIME = 0.2


class TestAdress(TestCase):

    def setUp(self) -> None:
        self.api = AdressApi()
        return super().setUp()

    def test_search(self) -> requests.Response:
        time.sleep(WAIT_TIME)
        r = self.api.search(q="8+bd+du+port", limit=15)
        self.assertTrue(r.status_code == 200)
        r = self.api.search(q="8+bd+du+port", postcode=44380, limit=15)
        self.assertTrue(r.status_code == 200)
        r = self.api.search(q="8+bd+du+port", type="street", limit=15)
        self.assertTrue(r.status_code == 200)
        return r

    def test_search_error(self) -> None:

        with self.assertRaises(ValueError):
            self.api.search(q="8+bd+du+port", type="noclue", limit=15)

    def test_reverse(self) -> requests.Response:
        time.sleep(WAIT_TIME)
        r = self.api.reverse(lon=2.37, lat=48.357)
        self.assertTrue(r.status_code == 200)
        return r

    def test_search_response(self) -> None:
        r = self.test_search()
        parsed = SearchResponse(**r.json())
        self.assertTrue(True)

    def test_reversed_response(self) -> None:
        r = self.test_reverse()
        parsed = ReverseResponse(**r.json())
        self.assertTrue(True)
