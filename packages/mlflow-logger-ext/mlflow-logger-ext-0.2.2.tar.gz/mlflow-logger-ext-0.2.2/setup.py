# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlflow_logger_ext', 'mlflow_logger_ext.external', 'mlflow_logger_ext.tests']

package_data = \
{'': ['*']}

install_requires = \
['gitpython', 'loguru', 'mlflow>=2.0,<3.0']

setup_kwargs = {
    'name': 'mlflow-logger-ext',
    'version': '0.2.2',
    'description': 'Using python decorator to manage MlFlow',
    'long_description': None,
    'author': 'seanyu',
    'author_email': 'weihsiang.yu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
