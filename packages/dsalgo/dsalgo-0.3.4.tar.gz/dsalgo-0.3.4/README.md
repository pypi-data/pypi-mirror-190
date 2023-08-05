
# dsalgo

A package for Datastructures and Algorithms written in Python.

[![Python package][ci-badge]][ci-url]
[![PyPI version][pypi-badge]][pypi-url]
[![License: MIT][mit-badge]][mit-url]
[![pre-commit][pre-commit-badge]][pre-commit-url]
[![Github pages][gh-pages-badge]][gh-pages-url]

[ci-badge]: https://github.com/kagemeka/dsalgo-python/actions/workflows/ci.yml/badge.svg
[ci-url]: https://github.com/kagemeka/dsalgo-python/actions/workflows/ci.yml
[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
[pre-commit-url]: https://github.com/pre-commit/pre-commit
[mit-badge]: https://img.shields.io/badge/License-MIT-blue.svg
[mit-url]: https://opensource.org/licenses/MIT
[pypi-badge]: https://badge.fury.io/py/dsalgo.svg
[pypi-url]: https://badge.fury.io/py/dsalgo
[gh-pages-badge]: https://github.com/kagemeka/dsalgo-python/actions/workflows/pages/pages-build-deployment/badge.svg
[gh-pages-url]: https://kagemeka.github.io/dsalgo-python

## Installation

```bash
python3 -m pip install -U dsalgo

# to use numba functionality for python <3.11
python3 -m pip install -U dsalgo[nb]

# for latest unstable version
python3 -m pip install -U git+git://github.com/kagemeka/dsalgo-python.git
```

## Development

```sh
docker compose up -d
```

(enter the container)

```sh
./setup.sh
source ~/.bashrc
```

CI before commit

```sh
./ci.sh
```

### documenting

```sh
poetry run pdoc dsalgo --show-source --math -o docs
```

### publish

```sh
poetry config pypi-token.pypi <your token> # only once
poetry build
poetry publish
```
