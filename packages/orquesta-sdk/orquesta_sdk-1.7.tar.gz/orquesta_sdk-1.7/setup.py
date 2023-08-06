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
    'version': '1.7',
    'description': 'No-code business rules and remote configurations',
    'long_description': '<p align="left">\n  <a href="https://orquesta.dev" target="_blank">\n    <img src="https://static.wixstatic.com/media/e063e5_4f60988535a643218a02ad84cf60b7cd~mv2.png/v1/fill/w_130,h_108,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/Logo%2001.png" alt="Orquesta"  height="84">\n  </a>\n</p>\n\n# Orquesta Python SDK\n\n**This library allows you to quickly and easily use the Orquesta API via Python.**\n\n# Installation\n\n## Prerequisites\n\n- Python version 2.7 and 3.5+\n- A free Orquesta account from [orquesta.dev](https://orquesta.dev).\n\n### Install package\n\n```bash\npip install orquestadev\n```\n\n## Dependencies\n\n- [requests](https://github.com/psf/requests)\n\n## Usage\n\n#### Query a rule with context\n\n```python\n\nimport os\nimport orquestadev\n\nclient = orquestadev.OrquestaClient(os.environ.get(\'ORQUESTA_API_KEY\'))\nresult = client.query(\'<your_rule_key>\', \'<your_default_value>\', {\'<your_field_key>\': \'<your_value>\'})\n\n## Example\n\nresult = client.query(\n            "kill_switch", false, {"environments": "production", "isAdmin": True}\n        )\n```\n\n#### Query a rule without context\n\n```python\n\nimport os\nimport orquestadev\n\nclient = orquestadev.OrquestaClient(os.environ.get(\'ORQUESTA_API_KEY\'))\nclient.query(\'<your_rule_key>\', \'<your_default_value>\')\n\n## Example\n\nresult = client.query("kill_switch", false)\n```\n',
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
