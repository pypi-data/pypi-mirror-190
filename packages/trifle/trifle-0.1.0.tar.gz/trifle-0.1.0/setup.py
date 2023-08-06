# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trifle']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'trifle',
    'version': '0.1.0',
    'description': 'Generate docker images using Python',
    'long_description': '# Trifle\n\nGenerate docker images using Python.\n\nWIP, more info to come.\n',
    'author': 'Maxwell Koo',
    'author_email': 'mjkoo90@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mjkoo/trifle',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
