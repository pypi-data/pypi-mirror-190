# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kaioretry']

package_data = \
{'': ['*']}

install_requires = \
['decorator>=5.1.1']

setup_kwargs = {
    'name': 'kaioretry',
    'version': '0.8.1',
    'description': 'All in one retry and aioretry decorators',
    'long_description': "# KaioRetry\n\n[![PyPI version](https://img.shields.io/pypi/v/kaioretry?logo=pypi&style=plastic)](https://pypi.python.org/pypi/kaioretry/)\n[![Supported Python Version](https://img.shields.io/pypi/pyversions/kaioretry?logo=python&style=plastic)](https://pypi.python.org/pypi/kaioretry/)\n[![License](https://img.shields.io/pypi/l/kaioretry?color=green&logo=GNU&style=plastic)](https://github.com/Anvil/kaioretry/blob/main/LICENSE)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/kaioretry?color=magenta&style=plastic)](https://pypistats.org/packages/kaioretry)\n[![Pylint Static Quality Github Action](https://github.com/Anvil/kaioretry/actions/workflows/pylint.yml/badge.svg)](https://github.com/Anvil/kaioretry/actions/workflows/pylint.yml)\n[![Pylint Static Quality Github Action](https://github.com/Anvil/kaioretry/actions/workflows/python-app.yml/badge.svg)](https://github.com/Anvil/kaioretry/actions/workflows/python-app.yml)\n\n\nKaioRetry is (yet another) retry decorator implementation, which is\nclearly inspired by the original\n[retry](https://pypi.org/project/retry) module and is actually\nbackward compatible with it.\n\nI say *backward* because, while `retry` clearly did the job for me for a\ntime, at some point I've encountered a big limitation: it did not work\nwith asyncio coroutines. And it's been unmaintained for 6 years.\n\nI found a few alternatives for that but none of them were both sync\nand async and since I did not wanted to use 2 differents modules for\nthe same goal, I've decided to write this one, with the rule that the\ncode duplication, between the sync and async versions, should be\nsmartly kept to a very very strict minimum.\n\nAnd here we are then.\n\n\n# Documentation\n\nAPI Documentation is available on readthedocs:\n[https://kaioretry.readthedocs.io/en/latest/]\n\n\n## TODO List\n\n* Write a decent README\n* Improve documentation display on the RTD\n",
    'author': 'Damien Nadé',
    'author_email': 'anvil.github+kaioretry@livna.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Anvil/kaioretry/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
