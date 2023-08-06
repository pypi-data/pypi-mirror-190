# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['autofake']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'autofake',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'Agustin Marquez',
    'author_email': 'agusdmb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/agusdmb/autofake',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
