from abc import ABC, abstractmethod


class Endpoint(object):
    def __init__(self, client):
        super(Endpoint, self).__init__()
        self.client = client

    @property
    @abstractmethod
    def _url(self) -> str:
        pass

    def _fetch(self, url: str, **kwargs: dict) -> dict:
        response = self.client.get(url, **kwargs)
        return response.json()

    @abstractmethod
    def __call__(self, *args: tuple, **kwargs: dict) -> dict:
        pass
