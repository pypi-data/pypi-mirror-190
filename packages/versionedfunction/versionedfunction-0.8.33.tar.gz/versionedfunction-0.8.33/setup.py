# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['versionedfunction']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'versionedfunction',
    'version': '0.8.33',
    'description': 'Sometimes you want to be able to dynamically call different versions of a function',
    'long_description': 'None',
    'author': 'John Heintz',
    'author_email': 'john@gistlabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
