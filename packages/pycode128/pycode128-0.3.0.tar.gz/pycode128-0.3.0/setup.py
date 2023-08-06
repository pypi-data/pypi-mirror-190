# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libs', 'pycode128', 'pycode128.cli_tools', 'tests']

package_data = \
{'': ['*'], 'libs': ['code128/*']}

install_requires = \
['click==8.0.1',
 'cloup>=0.15.1,<0.16.0',
 'termcolor>=1.1.0,<2.0.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['pycode128 = pycode128.cli_tools.cli:main']}

setup_kwargs = {
    'name': 'pycode128',
    'version': '0.3.0',
    'description': 'Python extension for Code128 barcode generator library.',
    'long_description': "# Code128 library's python extension\n\n\n[![pypi](https://img.shields.io/pypi/v/pycode128.svg)](https://pypi.org/project/pycode128/)\n[![python](https://img.shields.io/pypi/pyversions/pycode128.svg)](https://pypi.org/project/pycode128/)\n[![Build Status](https://github.com/gpongelli/pycode128/actions/workflows/dev.yml/badge.svg)](https://github.com/gpongelli/pycode128/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/gpongelli/pycode128/branch/main/graphs/badge.svg)](https://codecov.io/github/gpongelli/pycode128)\n\n\n\nPython extension for Code128 barcode generator library\n\n\n* Documentation: <https://gpongelli.github.io/pycode128>\n* GitHub: <https://github.com/gpongelli/pycode128>\n* PyPI: <https://pypi.org/project/pycode128/>\n* Free software: MIT\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n",
    'author': 'Gabriele Pongelli',
    'author_email': 'gabriele.pongelli@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gpongelli/pycode128',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
