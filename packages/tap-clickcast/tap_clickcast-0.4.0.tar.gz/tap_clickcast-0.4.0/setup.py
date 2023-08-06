# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_clickcast', 'tap_clickcast.tests']

package_data = \
{'': ['*'], 'tap_clickcast': ['schemas/*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['tap-clickcast = tap_clickcast.tap:TapClickcast.cli']}

setup_kwargs = {
    'name': 'tap-clickcast',
    'version': '0.4.0',
    'description': '`tap-clickcast` is a Singer tap for clickcast, built with the Meltano SDK for Singer Taps.',
    'long_description': 'None',
    'author': 'Datateer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
