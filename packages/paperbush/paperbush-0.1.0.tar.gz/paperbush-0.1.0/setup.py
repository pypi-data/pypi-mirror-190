# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['paperbush']

package_data = \
{'': ['*'],
 'paperbush': ['.mypy_cache/*',
               '.mypy_cache/3.9/*',
               '.mypy_cache/3.9/_typeshed/*',
               '.mypy_cache/3.9/collections/*',
               '.mypy_cache/3.9/ctypes/*',
               '.mypy_cache/3.9/email/*',
               '.mypy_cache/3.9/importlib/*',
               '.mypy_cache/3.9/importlib/metadata/*',
               '.mypy_cache/3.9/os/*',
               '.mypy_cache/3.9/paperbush/*']}

setup_kwargs = {
    'name': 'paperbush',
    'version': '0.1.0',
    'description': 'Dead easy argument parsing',
    'long_description': 'None',
    'author': 'trag1c',
    'author_email': 'trag1cdev@yahoo.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
