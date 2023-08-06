# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pygraph']
install_requires = \
['twine==4.0.1']

setup_kwargs = {
    'name': 'pygraph-touge',
    'version': '0.1.0',
    'description': 'Simple Python Graph Library',
    'long_description': 'None',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
