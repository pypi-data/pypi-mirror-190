# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snowiecaster', 'snowiecaster.backends', 'snowiecaster.backends.memory']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snowiecaster',
    'version': '0.1.0',
    'description': '',
    'long_description': "# SnowieCaster\nThis library is created for Snowie project to use Ariadne library.\n\nIt currently only supports in-memory backend, but it isn't release version\n\n## Requirements\nPython 3.6+\n## Installation\n* `pip install snowiecaster`\n#\n",
    'author': 'AndreiErshov',
    'author_email': 'mtaprovince04@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
