# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pykorean']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.1,<8.0.0']

entry_points = \
{'console_scripts': ['korean = pykorean.main:cli']}

setup_kwargs = {
    'name': 'pykorean',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'codemke',
    'author_email': 'altoformula@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
