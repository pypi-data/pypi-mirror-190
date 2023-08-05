# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctflib', 'ctflib.crypto']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ctflib',
    'version': '0.1.2',
    'description': 'Tools for better CTF experience',
    'long_description': '# ctflib\n',
    'author': 'Alexey Tarasov',
    'author_email': 'tarasovion2004@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/LeKSuS-04/ctflib',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
