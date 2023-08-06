from types import SimpleNamespace

import httpx

from ._bolsa import bolsa
from ._tesouro import tesouro


class Fintz(object):
    def __init__(self, key: str = None):
        super(Fintz, self).__init__()
        self.key = key or '29kWWEfWHB6wjtsGYCLWn9PJ8seFzgtR2Ju9UvyH'

        self.client = httpx.Client(
            base_url='https://api.fintz.com.br',
            headers={'X-Api-Key': self.key},
            timeout=10  # seconds
        )

        self.bolsa = bolsa(self.client)
        self.titulos = SimpleNamespace(tesouro=tesouro(self.client))

    def __del__(self):
        self.client.close()
