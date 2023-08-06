# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boxobj_image']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0', 'boxobj>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'boxobj-image',
    'version': '0.1.0',
    'description': 'Utilities to support working with boxobj classes and Pillow images',
    'long_description': '',
    'author': 'dschultz0',
    'author_email': 'dave@daveschultzconsulting.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
