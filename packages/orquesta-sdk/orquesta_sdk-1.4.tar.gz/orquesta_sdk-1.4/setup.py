# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orquesta_sdk']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'orquesta-sdk',
    'version': '1.4',
    'description': 'No-code business rules and remote configurations',
    'long_description': 'None',
    'author': 'Orquesta',
    'author_email': 'info@orquesta.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
