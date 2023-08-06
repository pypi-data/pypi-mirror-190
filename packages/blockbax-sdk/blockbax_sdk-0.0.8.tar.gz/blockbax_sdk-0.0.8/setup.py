# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['blockbax_sdk',
 'blockbax_sdk.client',
 'blockbax_sdk.client.api',
 'blockbax_sdk.models',
 'blockbax_sdk.util']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3',
 'python-dateutil>=2.8.2',
 'pytz>=2022.7.1',
 'tenacity>=8.1.0',
 'typing-extensions>=4.4.0']

entry_points = \
{'console_scripts': ['bx = blockbax_sdk.console:main',
                     'get_subjects = blockbax_sdk.console:get_subjects',
                     'user-agent = blockbax_sdk.console:user_agent']}

setup_kwargs = {
    'name': 'blockbax-sdk',
    'version': '0.0.8',
    'description': 'Blockbax Python SDK',
    'long_description': '# Blockbax Python SDK\n\nFor more information please refer to our [Python SDK documentation](https://blockbax.com/docs/integrations/python-sdk/).\n',
    'author': 'Blockbax',
    'author_email': 'development@blockbax.com',
    'maintainer': 'Blockbax',
    'maintainer_email': 'development@blockbax.com',
    'url': 'https://blockbax.com/docs/integrations/python-sdk/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
