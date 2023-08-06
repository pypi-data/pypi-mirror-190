# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semithuesystem']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'semithuesystem',
    'version': '1.0.2',
    'description': 'This package is a representation of a string rewriting system, historically called the Semi-Thue System.',
    'long_description': '# Semi-Thue System\nhttps://en.wikipedia.org/wiki/Semi-Thue_system',
    'author': 'pab-h',
    'author_email': 'dev.pab.2020@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pab-h/semithuesystem',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
