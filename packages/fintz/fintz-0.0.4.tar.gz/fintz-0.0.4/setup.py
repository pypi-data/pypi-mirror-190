# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fintz']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0']

setup_kwargs = {
    'name': 'fintz',
    'version': '0.0.4',
    'description': 'Python client to interact with Fintz API',
    'long_description': "# Fintz SDK\n\nBiblioteca python para você interagir com a API da Fintz\n\n## Sobre\n\nA fintz é uma API feita para você não ter que se preocupar com dados do mercado\nfinanceiro. É fácil de usar e você pode começar a construir ferramentas e\nserviços rapidamente.\n\nPara mais informações, entre em contato conosco pelo nosso [site][1].\n\n## Instalar\n\nA instalação é super simples, basta usar `pip`:\n\n```\npip install fintz\n```\n\n## Como usar?\n\nEstamos sempre trabalhando para melhorar a usabilidade do SDK. Queremos deixar\nbem intuitivo para qualquer pessoa. Desde desenvolvedores com experiência até\npessoas com baixo conhecimento na área de programação.\n\nAqui vão alguns exemplos de métodos que temos implementados:\n\n```py\nfrom fintz import Fintz\n\nfintz = Fintz()  # usa uma chave padrão limitada\n\nfintz.bolsa.dres('PETR4', year=2020, quarter=3)\nfintz.bolsa.info('PETR4')\nfintz.bolsa.busca('PETR4')\nfintz.bolsa.eventos('PETR4')\nfintz.bolsa.cotacoes('PETR4')\nfintz.bolsa.historico('PETR4')\nfintz.bolsa.proventos('PETR4')\n\nfintz.titulos.tesouro.info('NTNBP20450515')\nfintz.titulos.tesouro.cupons('NTNB20450515')\nfintz.titulos.tesouro.busca()\nfintz.titulos.tesouro.precos.atual('NTNBP20450515')\nfintz.titulos.tesouro.precos.historico('NTNBP20450515')\n```\n\nSe você estiver recebendo erros do tipo `429 Too Many Requests`, significa que\na chave padrão está sendo muito utilizada e você deverá entrar em contato\nconosco para conseguir uma chave nova com limites maiores. Para entrar em\ncontato, use o formulário em nosso [site][1].\n\nQuando tiver a chave nova, basta usar o SDK da seguinte forma:\n\n```py\nfrom fintz import Fintz\n\nfintz = Fintz('SUA_CHAVE_AQUI')\n```\n\n[1]: https://fintz.com.br/\n",
    'author': 'João Vicente Meyer',
    'author_email': '1994meyer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
