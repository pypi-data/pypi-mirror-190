# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['salesman',
 'salesman.admin',
 'salesman.admin.wagtail',
 'salesman.basket',
 'salesman.basket.migrations',
 'salesman.checkout',
 'salesman.core',
 'salesman.orders',
 'salesman.orders.migrations']

package_data = \
{'': ['*'],
 'salesman.admin': ['static/salesman/admin/*',
                    'templates/salesman/admin/*',
                    'templates/salesman/admin/includes/*']}

install_requires = \
['django>=3.1,<4.2', 'djangorestframework>=3.11,<3.15']

extras_require = \
{'docs': ['wagtail>=2.9,<4.2',
          'sphinx>=4.4.0,<4.5.0',
          'sphinx-rtd-theme>=1.0.0,<1.1.0',
          'sphinx-autobuild>=2021.3.0,<2021.4.0',
          'sphinxcontrib-httpdomain>=1.8.0,<1.9.0'],
 'example': ['Pygments>=2.6,<3.0', 'wagtail>=2.9,<4.2'],
 'pygments': ['Pygments>=2.6,<3.0'],
 'tests': ['Pygments>=2.6,<3.0',
           'wagtail>=2.9,<4.2',
           'pytest>=7.0.0,<7.1.0',
           'pytest-django>=4.5.0,<4.6.0',
           'pytest-cov>=3.0.0,<3.1.0']}

setup_kwargs = {
    'name': 'django-salesman',
    'version': '1.1.6',
    'description': 'Headless e-commerce framework for Django and Wagtail.',
    'long_description': '<p align="center">\n    <a href="https://django-salesman.readthedocs.org/">\n        <img src="https://cdn.jsdelivr.net/gh/dinoperovic/django-salesman@master/docs/_static/logo.svg" width="250" alt="Salesman logo">\n    </a>\n</p>\n<h3 align="center">Headless e-commerce framework for Django and Wagtail.</h3>\n<p align="center">\n    <a href="https://pypi.org/project/django-salesman/">\n        <img alt="PyPI" src="https://img.shields.io/pypi/v/django-salesman">\n    </a>\n    <a href="https://github.com/dinoperovic/django-salesman/actions?query=workflow:Test">\n        <img alt="GitHub - Test status" src="https://github.com/dinoperovic/django-salesman/actions/workflows/test.yml/badge.svg">\n    </a>\n    <a href="http://codecov.io/github/dinoperovic/django-salesman">\n        <img alt="Codecov branch" src="https://img.shields.io/codecov/c/github/dinoperovic/django-salesman/master">\n    </a>\n    <a href="https://pypi.org/project/django-salesman/">\n        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/django-salesman">\n    </a>\n    <a href="https://pypi.org/project/django-salesman/">\n        <img alt="PyPI - Django Version" src="https://img.shields.io/pypi/djversions/django-salesman">\n    </a>\n    <a href="https://github.com/psf/black">\n        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n    </a>\n</p>\n\n**Salesman** provides a configurable system for building an online store.\nIt includes a **RESTful** API with endpoints for manipulating the basket,\nprocessing the checkout and payment operations as well as managing customer orders.\n\n## Features\n\n- API endpoints for **Basket**, **Checkout** and **Order**\n- Support for as many **Product** types needed using generic relations\n- Pluggable **Modifier** system for basket processing\n- **Payment** methods interface to support any gateway necessary\n- Customizable **Order** implementation\n- Fully swappable **Order** and **Basket** models\n- [Wagtail](https://wagtail.io/) and **Django** admin implementation\n\n## Documentation\n\nDocumentation is available on [Read the Docs](https://django-salesman.readthedocs.org).\n',
    'author': 'Dino Perovic',
    'author_email': 'dino.perovic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/django-salesman/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
