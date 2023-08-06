from types import SimpleNamespace
from datetime import date

from ._base import Endpoint


class Info(Endpoint):
    _url = '/titulos-publicos/tesouro/%s/informacoes/'

    def __call__(self, code: str) -> dict:
        url = self._url % code.upper()
        return self._fetch(url)


class Cupons(Endpoint):
    _url = '/titulos-publicos/tesouro/%s/cupons/'

    def __call__(self, code: str) -> dict:
        url = self._url % code.upper()
        return self._fetch(url)['dados']


class Busca(Endpoint):
    _url = '/titulos-publicos/tesouro/'

    def __call__(self) -> dict:
        return self._fetch(self._url)['dados']


class PrecoAtual(Endpoint):
    _url = '/titulos-publicos/tesouro/%s/precos/historico/'

    def __call__(self, code: str) -> dict:
        url = self._url % code.upper()
        return self._fetch(url)


class PrecoHistorico(Endpoint):
    _url = '/titulos-publicos/tesouro/%s/precos/historico/'

    def __call__(self, code: str, start: date = None, end: date = None) -> dict:
        url = self._url % code.upper()
        params = {'dataInicio': start, 'dataFim': end}
        params = {k: v for k, v in params.items() if v is not None}
        return self._fetch(url)['dados']


def tesouro(client) -> SimpleNamespace:
    precos = SimpleNamespace(
        atual=PrecoAtual(client),
        historico=PrecoHistorico(client),
    )

    return SimpleNamespace(
        info=Info(client),
        cupons=Cupons(client),
        busca=Busca(client),
        precos=precos
    )
