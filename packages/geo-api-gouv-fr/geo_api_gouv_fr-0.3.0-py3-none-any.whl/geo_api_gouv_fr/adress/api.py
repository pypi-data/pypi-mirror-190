import requests
from .schemas import (
    SearchParams,
    ReverseParams
)


class Api:
    """
    Documentation : https://adresse.data.gouv.fr/api-doc/adresse
    """

    def __init__(self, **kwargs):
        self.url = kwargs.get("url", "https://api-adresse.data.gouv.fr")

    def search(self, **kwargs) -> requests.Response:
        params = SearchParams(**kwargs)
        return requests.get(self.url + "/search", params=params.dict())

    def reverse(self, **kwargs) -> requests.Response:
        params = ReverseParams(**kwargs)
        return requests.get(self.url + "/reverse", params=params.dict())
