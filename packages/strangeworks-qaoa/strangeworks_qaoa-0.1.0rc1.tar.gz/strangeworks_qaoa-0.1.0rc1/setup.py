# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strangeworks_qaoa']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=3.0,<4.0',
 'numpy==1.23.2',
 'qiskit>=0.41.0,<0.42.0',
 'strangeworks==0.4.0rc1']

setup_kwargs = {
    'name': 'strangeworks-qaoa',
    'version': '0.1.0rc1',
    'description': 'Extension to strangeworks sdk to allow user to run qaoa service',
    'long_description': '# Strangeworks QAOA SDK Extension\n\nThis extension provides access to the Strangeworks QAOA service through the SDK.\n\n## Installation\n\nInstall using `poetry`\n\n```\npip install poetry\npoetry install \n```\n\n## Tests\n\nTest using pytest\n```\npoetry run pytest tests\n```\n\n## Lint\n\nLint with black\n```\npoetry run black .\n```\n\n## Bump version\n\nBump version with [poetry](https://python-poetry.org/docs/cli/#version).\n\n```\npoetry version [patch, minor, major]\n```\n\n## Update packages\n\nUpdate <package> version\n```\npoetry update <package>\n```\n\nUpdate all packages\n```\npoetry update\n```\n',
    'author': 'SFlann',
    'author_email': 'stuart@strangeworks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
