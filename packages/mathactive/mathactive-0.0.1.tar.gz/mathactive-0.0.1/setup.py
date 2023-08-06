# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mathactive']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.89.1,<0.90.0',
 'jupyter>=1.0,<2.0',
 'pandas>=1.5,<2.0',
 'scikit-learn>=1.2,<2.0',
 'spacy>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'mathactive',
    'version': '0.0.1',
    'description': 'Conversational math active learning.',
    'long_description': None,
    'author': 'hobs',
    'author_email': 'hobson@totalgood.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
