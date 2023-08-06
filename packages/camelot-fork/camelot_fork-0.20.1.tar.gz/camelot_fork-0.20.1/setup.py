# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['camelot', 'camelot.backends', 'camelot.parsers']

package_data = \
{'': ['*']}

install_requires = \
['chardet>=5.1.0,<6.0.0',
 'click>=8.0.1',
 'numpy>=1.24.2,<2.0.0',
 'openpyxl>=3.1.0,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pdfminer-six>=20221105,<20221106',
 'pypdf>=3.4.0,<4.0.0',
 'tabulate>=0.9.0,<0.10.0']

entry_points = \
{'console_scripts': ['camelot = camelot.__main__:main']}

setup_kwargs = {
    'name': 'camelot-fork',
    'version': '0.20.1',
    'description': 'Camelot Fork',
    'long_description': "# Camelot Fork\n\n[![PyPI](https://img.shields.io/pypi/v/camelot-fork.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/camelot-fork.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/camelot-fork)][python version]\n[![License](https://img.shields.io/pypi/l/camelot-fork)][license]\n\n[![Read the documentation at https://camelot-fork.readthedocs.io/](https://img.shields.io/readthedocs/camelot-fork/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/foarsitter/camelot-fork/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/foarsitter/camelot-fork/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/camelot-fork/\n[status]: https://pypi.org/project/camelot-fork/\n[python version]: https://pypi.org/project/camelot-fork\n[read the docs]: https://camelot-fork.readthedocs.io/\n[tests]: https://github.com/foarsitter/camelot-fork/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/foarsitter/camelot-fork\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Camelot Fork_ via [pip] from [PyPI]:\n\n```console\n$ pip install camelot-fork\n```\n\n## Usage\n\nPlease see the [Command-line Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Camelot Fork_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/foarsitter/camelot-fork/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/foarsitter/camelot-fork/blob/main/LICENSE\n[contributor guide]: https://github.com/foarsitter/camelot-fork/blob/main/CONTRIBUTING.md\n[command-line reference]: https://camelot-fork.readthedocs.io/en/latest/usage.html\n",
    'author': 'Jelmer Draaijer',
    'author_email': 'info@jelmert.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/foarsitter/camelot-fork',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
