# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hltv_stats']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'cuid>=0.3,<0.4', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'hltv-stats',
    'version': '0.1.4',
    'description': 'Simple parser for HLTV.org team stats and matches (using requests and bs4)',
    'long_description': 'Simple parser for HLTV.org team stats and matches (using requests and bs4)',
    'author': 'Armen A',
    'author_email': 'agalyan.armen@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/a3agalyan/hltv-stats',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
