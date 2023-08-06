# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zktlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zktlib',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'askdjajf aslkda',
    'author_email': 'no@mail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
