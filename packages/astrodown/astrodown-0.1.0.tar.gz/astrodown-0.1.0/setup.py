# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astrodown']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'astrodown',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Qiushi Yan',
    'author_email': 'qiushi.yann@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
