# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gundi_client']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8,<4.0', 'environs>=9.5,<10.0', 'pydantic>=1.10,<2.0']

setup_kwargs = {
    'name': 'gundi-client',
    'version': '0.2.1',
    'description': "An async client for Gundi's API",
    'long_description': "# gundi-client\nA python client for Gundi's API\n",
    'author': 'Rohit Chaudhri',
    'author_email': 'rohitc@vulcan.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
