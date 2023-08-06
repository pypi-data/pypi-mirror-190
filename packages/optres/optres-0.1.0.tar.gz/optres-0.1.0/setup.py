# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optres']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'optres',
    'version': '0.1.0',
    'description': "Yet another Rust's Option<T> and Result<T, E> simple implementation in Python.",
    'long_description': '\n# optres\n\n`Yet another Rust\'s Option<T> and Result<T, E> simple implementation in Python.`\n\n[![Python package][ci-badge]][ci-url]\n[![PyPI version][pypi-badge]][pypi-url]\n[![License: MIT][license-badge]][license-url]\n[![pre-commit][pre-commit-badge]][pre-commit-url]\n[![Github pages][gh-pages-badge]][gh-pages-url]\n\n[ci-badge]: https://github.com/kagemeka/optres/actions/workflows/ci.yml/badge.svg\n[ci-url]: https://github.com/kagemeka/optres/actions/workflows/ci.yml\n[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n[pre-commit-url]: https://github.com/pre-commit/pre-commit\n[license-badge]: https://img.shields.io/badge/License-Apache2.0-green.svg\n[license-url]: https://opensource.org/licenses/Apache2.0\n[pypi-badge]: https://badge.fury.io/py/optres.svg\n[pypi-url]: https://badge.fury.io/py/optres\n[gh-pages-badge]: https://github.com/kagemeka/optres/actions/workflows/pages/pages-build-deployment/badge.svg\n[gh-pages-url]: https://kagemeka.github.io/optres\n\n## Installation\n\n```bash\npython3 -m pip install -U optres\n```\n\n## Example\n\n```py\nfrom optres import unwrap, Result, Err, is_ok, is_err, unwrap_err\nfrom typing import LiteralString\n\n\ndef return_result(x: int | None) -> Result[int, LiteralString]:\n    return Err("not int") if x is None else x\n\n\ndef example() -> None:\n    a: int | None = 1\n    c: int = unwrap(a)\n    print(c)\n    assert is_ok(return_result(a))\n    a = None\n    # unwrap(a) # error := panic in Rust.\n    may_be_err = return_result(a)\n    assert is_err(may_be_err)\n    print(unwrap_err(may_be_err))\n\n\nif __name__ == "__main__":\n    example()\n\n```\n',
    'author': 'kagemeka',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kagemeka/optres#readme',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
