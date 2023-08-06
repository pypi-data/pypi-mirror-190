from types import SimpleNamespace
from datetime import date

from ._base import Endpoint


class Dres(Endpoint):
    _url = '/bolsa/b3/%s/dres/'

    def __call__(self, ticker: str, year: int, quarter: int) -> dict:
        url = self._url % ticker.upper()
        params = {'year': year, 'quarter': quarter}
        return self._fetch(url, params=params)


class Info(Endpoint):
    _url = '/bolsa/b3/%s/info/'

    def __call__(self, ticker: str) -> dict:
        url = self._url % ticker.upper()
        return self._fetch(url)


class Busca(Endpoint):
    _url = '/bolsa/b3/'

    def __call__(self, q: str) -> dict:
        params = {'q': q}
        return self._fetch(self._url, params=params)


class Eventos(Endpoint):
    _url = '/bolsa/b3/%s/eventos/'

    def __call__(self, ticker: str, start: date = None, end: date = None) -> dict:
        url = self._url % ticker.upper()
        params = {'dataInicio': start, 'dataFim': end}
        params = {k: v for k, v in params.items() if v is not None}
        return self._fetch(url, params=params)['dados']


class Cotacoes(Endpoint):
    _url = '/bolsa/b3/%s/cotacoes/'

    def __call__(self, ticker: str) -> dict:
        url = self._url % ticker.upper()
        return self._fetch(url)


class Historico(Endpoint):
    _url = '/bolsa/b3/%s/historico/'

    def __call__(
        self,
        ticker: str,
        start: date = None,
        end: date = None,
        page: int = 1,
        size: int = 10
    ) -> dict:
        url = self._url % ticker.upper()
        params = {'dataInicio': start, 'dataFim': end, 'pagina': page, 'tamanho': size}
        params = {k: v for k, v in params.items() if v is not None}
        return self._fetch(url, params=params)['dados']


class Proventos(Endpoint):
    _url = '/bolsa/b3/%s/proventos/'

    def __call__(self, ticker: str, start: date = None, end: date = None) -> dict:
        url = self._url % ticker.upper()
        params = {'dataInicio': start, 'dataFim': end}
        params = {k: v for k, v in params.items() if v is not None}
        return self._fetch(url, params=params)['dados']


def bolsa(client):
    return SimpleNamespace(
        dres=Dres(client),
        info=Info(client),
        busca=Busca(client),
        eventos=Eventos(client),
        cotacoes=Cotacoes(client),
        historico=Historico(client),
        proventos=Proventos(client)
    )
