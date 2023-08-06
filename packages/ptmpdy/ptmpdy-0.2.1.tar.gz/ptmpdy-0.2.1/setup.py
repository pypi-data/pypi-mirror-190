# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ptmpdy']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=6.0,<7.0',
 'rich>=12.6.0,<13.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['ptmpdy = ptmpdy.main:app']}

setup_kwargs = {
    'name': 'ptmpdy',
    'version': '0.2.1',
    'description': '',
    'long_description': '# ptmpdy\n\n[![PyPI version](https://badge.fury.io/py/ptmpdy.svg)](https://badge.fury.io/py/ptmpdy)\n[![Workflow on new release published](https://github.com/hayata-yamamoto/ptmpdy/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/hayata-yamamoto/ptmpdy/actions/workflows/pypi-publish.yml)\n\nptmpdy project is aiming to reduce troubles in serverless stack operations.\n\n"ptmpdy" is "Please Tell Me Path Declaration in Yaml"\n\n## Overview\n\nThis CLI tools provide code generation experience.\n\nIf you have a [serverless.yml](tests/test_data/serverless.yml) to host your lambda application, ptmpdy provides Python Enum objects like\n\n```python\nfrom enum import Enum\n\n\nclass LambdaHandlers(str, Enum):\n    sample_handler = "sample-service-sample-handler"\n    sample_handler2 = "sample-service-sample-handler2"\n\n```\n\n## Usage\n\nPlease see [usage.md](docs/usage.md).\n\n## Project Scope\n\nServerless Framework\n\n- [x] Adding to Python code generation from `serverless.yml`\n- [ ] Adding serverless plugin\n\n## Development\n\n```bash\npoetry install\n```\n\n## Contributions\n\nThis project is welcome to contribute. When you want to contribute this project, please follow contribute guides.\n\n**Guides**\n\n1. Vote issues\n2. Create a PR to main branch in assigning to @hayata-yamamoto as a reviewer\n',
    'author': 'hayata-yamamoto',
    'author_email': 'hayata.yamamoto.work@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
