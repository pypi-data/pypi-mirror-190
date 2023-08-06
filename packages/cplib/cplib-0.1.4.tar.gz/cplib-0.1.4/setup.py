# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cplib']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'scipy']

extras_require = \
{'nb:python_version < "3.11"': ['numba>=0.56,<0.57']}

setup_kwargs = {
    'name': 'cplib',
    'version': '0.1.4',
    'description': '',
    'long_description': 'None',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
