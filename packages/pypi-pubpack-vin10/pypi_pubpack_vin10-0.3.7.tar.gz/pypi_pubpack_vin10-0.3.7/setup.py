# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_demo']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5,<2.0.0']

setup_kwargs = {
    'name': 'pypi-pubpack-vin10',
    'version': '0.3.7',
    'description': 'Upload Python package to PyPI (demo)',
    'long_description': '# pypi-test',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
