# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cgepy', 'cgepy.unstable']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cgepy',
    'version': '0.5.9',
    'description': 'Tools for developing graphical programs inside the console.',
    'long_description': '',
    'author': 'catbox305',
    'author_email': 'lion712yt@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
