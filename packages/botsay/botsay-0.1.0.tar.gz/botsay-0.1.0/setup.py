# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botsay']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.6,<0.5.0', 'lolpython>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['botsay = botsay.main:run']}

setup_kwargs = {
    'name': 'botsay',
    'version': '0.1.0',
    'description': 'cowsay but with no cows and a lot of robots',
    'long_description': 'idk :)',
    'author': 'RoboM101',
    'author_email': 'personal@robom101.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
