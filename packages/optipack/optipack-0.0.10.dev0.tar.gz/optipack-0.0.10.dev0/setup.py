# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optipack', 'optipack.sdk']

package_data = \
{'': ['*'], 'optipack': ['.config/*']}

install_requires = \
['typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['optipack = optipack.cli:run']}

setup_kwargs = {
    'name': 'optipack',
    'version': '0.0.10.dev0',
    'description': 'The optimal package for ML at OM',
    'long_description': '![optipack](asset/image/logo.png)\n\n# What optipack do: \n- Create base folder structure follow the project and environment\n- Generate rough hyperparam.yml template',
    'author': 'indigoYoshimaru',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
