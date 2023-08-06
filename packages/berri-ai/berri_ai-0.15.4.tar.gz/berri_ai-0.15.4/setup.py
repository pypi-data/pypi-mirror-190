# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berri_ai']

package_data = \
{'': ['*']}

install_requires = \
['gpt-index>=0.3.6,<0.4.0',
 'html2text>=2020.1.16,<2021.0.0',
 'mixpanel>=4.10.0,<5.0.0',
 'pipreqs>=0.4.11,<0.5.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'berri-ai',
    'version': '0.15.4',
    'description': '',
    'long_description': None,
    'author': 'Team Berri',
    'author_email': 'clerkieai@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
