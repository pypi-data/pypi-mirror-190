# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mightstone', 'mightstone.rule', 'mightstone.services']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'aiohttp-client-cache>=0.8.1,<0.9.0',
 'aiostream>=0.4.5,<0.5.0',
 'asyncstdlib>=3.10.5,<4.0.0',
 'beanie>=1.17.0,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'ijson>=3.2.0.post0,<4.0.0',
 'nest-asyncio>=1.5.6,<2.0.0',
 'ordered-set>=4.1.0,<5.0.0',
 'pytest>=7.2.1,<8.0.0',
 'python-slugify>=8.0.0,<9.0.0']

entry_points = \
{'console_scripts': ['mightstone = mightstone.cli:cli']}

setup_kwargs = {
    'name': 'mightstone',
    'version': '0.1.3',
    'description': 'A library manage all things Magic The Gathering related in python',
    'long_description': '# mightstone\n\n\n[![PyPi](https://img.shields.io/pypi/v/mightstone.svg)](https://pypi.python.org/pypi/mightstone)\n[![Travis](https://img.shields.io/travis/guibod/mightstone.svg)](https://travis-ci.com/guibod/mightstone)\n[![Documentation](https://readthedocs.org/projects/mightstone/badge/?version=latest)](https://mightstone.readthedocs.io/en/latest/?badge=latest)\n[![Updates](https://pyup.io/repos/github/guibod/mightstone/shield.svg)](https://pyup.io/repos/github/guibod/mightstone/)\n[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)\n\nA library manage all things Magic The Gathering related in python\n\n\n## Developing\n\nRun `make` for help\n\n    make install             # Run `poetry install`\n    make showdeps            # run poetry to show deps\n    make lint                # Runs bandit and black in check mode\n    make format              # Formats you code with Black\n    make test                # run pytest with coverage\n    make build               # run `poetry build` to build source distribution and wheel\n    make pyinstaller         # Create a binary executable using pyinstaller\n',
    'author': 'Guillaume Boddaert',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/guibod/mightstone',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
