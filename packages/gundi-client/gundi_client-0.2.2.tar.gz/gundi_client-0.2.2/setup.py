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
    'version': '0.2.2',
    'description': "An async client for Gundi's API",
    'long_description': '# Gundi Client\n## Introduction\n[Gundi](https://www.earthranger.com/), a.k.a "The Portal" is a platform to manage integrations.\nThe gundi-client is an async python client to interact with Gundi\'s REST API.\n\n## Installation\n```\npip install gundi-client\n```\n\n## Usage\n\n```\nimport aiohttp\nfrom gundi_client import PortalApi\n\nasync with aiohttp.ClientSession() as session:\n    try:\n        response = await portal.get_outbound_integration_list(\n            session=session, inbound_id=str(inbound_id), device_id=str(device_id)\n        )\n    except aiohttp.ServerTimeoutError as e:\n        logger.error("Read Timeout")              \n        ...\n    except aiohttp.ClientResponseError as e:\n        logger.exception("Failed to get outbound integrations for inbound_id")\n        ..\n    else:\n        # response contains a list configs as dicts\n        for integration in response:  \n            .. \n```\n',
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
