# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resources']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'module-resource',
    'version': '0.1.1',
    'description': 'load resources from module',
    'long_description': 'load resources from module',
    'author': 'jawide',
    'author_email': '596929059@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
