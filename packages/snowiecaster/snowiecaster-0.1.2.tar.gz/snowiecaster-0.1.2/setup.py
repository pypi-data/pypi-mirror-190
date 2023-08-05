# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snowiecaster', 'snowiecaster.backends', 'snowiecaster.backends.memory']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.991,<0.992',
 'pylint>=2.16.1,<3.0.0',
 'pytest-asyncio>=0.20.3,<0.21.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest-order>=1.0.1,<2.0.0',
 'pytest-profiling>=1.7.0,<2.0.0',
 'pytest>=7.2.1,<8.0.0']

setup_kwargs = {
    'name': 'snowiecaster',
    'version': '0.1.2',
    'description': 'An easy pub/sub python library',
    'long_description': "# SnowieCaster\nThis library was made for Snowie project to use Ariadne library.\n\nIt currently supports only in-memory backend, but it isn't release version\n\n## Requirements\nPython 3.6+\n## Installation\n* `pip install snowiecaster`\n\n",
    'author': 'AndreiErshov',
    'author_email': 'mtaprovince04@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
