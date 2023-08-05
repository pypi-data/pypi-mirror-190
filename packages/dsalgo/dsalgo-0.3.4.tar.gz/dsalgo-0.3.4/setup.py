# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dsalgo']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'scipy']

extras_require = \
{'nb:python_version < "3.11"': ['numba>=0.56,<0.57']}

setup_kwargs = {
    'name': 'dsalgo',
    'version': '0.3.4',
    'description': 'A package for datastructures and algorithms.',
    'long_description': '\n# dsalgo\n\nA package for Datastructures and Algorithms written in Python.\n\n[![Python package][ci-badge]][ci-url]\n[![PyPI version][pypi-badge]][pypi-url]\n[![License: MIT][mit-badge]][mit-url]\n[![pre-commit][pre-commit-badge]][pre-commit-url]\n[![Github pages][gh-pages-badge]][gh-pages-url]\n\n[ci-badge]: https://github.com/kagemeka/dsalgo-python/actions/workflows/ci.yml/badge.svg\n[ci-url]: https://github.com/kagemeka/dsalgo-python/actions/workflows/ci.yml\n[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n[pre-commit-url]: https://github.com/pre-commit/pre-commit\n[mit-badge]: https://img.shields.io/badge/License-MIT-blue.svg\n[mit-url]: https://opensource.org/licenses/MIT\n[pypi-badge]: https://badge.fury.io/py/dsalgo.svg\n[pypi-url]: https://badge.fury.io/py/dsalgo\n[gh-pages-badge]: https://github.com/kagemeka/dsalgo-python/actions/workflows/pages/pages-build-deployment/badge.svg\n[gh-pages-url]: https://kagemeka.github.io/dsalgo-python\n\n## Installation\n\n```bash\npython3 -m pip install -U dsalgo\n\n# to use numba functionality for python <3.11\npython3 -m pip install -U dsalgo[nb]\n\n# for latest unstable version\npython3 -m pip install -U git+git://github.com/kagemeka/dsalgo-python.git\n```\n\n## Development\n\n```sh\ndocker compose up -d\n```\n\n(enter the container)\n\n```sh\n./setup.sh\nsource ~/.bashrc\n```\n\nCI before commit\n\n```sh\n./ci.sh\n```\n\n### documenting\n\n```sh\npoetry run pdoc dsalgo --show-source --math -o docs\n```\n\n### publish\n\n```sh\npoetry config pypi-token.pypi <your token> # only once\npoetry build\npoetry publish\n```\n',
    'author': 'kagemeka',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kagemeka/dsalgo-python#readme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
