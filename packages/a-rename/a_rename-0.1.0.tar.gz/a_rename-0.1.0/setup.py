# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['a_rename']

package_data = \
{'': ['*']}

install_requires = \
['debugpy>=1.6.6,<2.0.0']

setup_kwargs = {
    'name': 'a-rename',
    'version': '0.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Matheus Henrique',
    'author_email': 'matheus2hcosta@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
