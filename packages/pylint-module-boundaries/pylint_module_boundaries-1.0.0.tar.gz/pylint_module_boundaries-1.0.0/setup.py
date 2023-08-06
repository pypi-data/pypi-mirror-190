# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylint_module_boundaries']

package_data = \
{'': ['*']}

install_requires = \
['pylint>=2,<3']

setup_kwargs = {
    'name': 'pylint-module-boundaries',
    'version': '1.0.0',
    'description': '',
    'long_description': 'None',
    'author': 'DetachHead',
    'author_email': 'detachhead@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
