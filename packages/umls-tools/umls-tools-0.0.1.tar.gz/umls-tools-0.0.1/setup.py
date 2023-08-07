# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umls_tools', 'umls_tools.metathesaurus', 'umls_tools.semantic_network']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'umls-tools',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Tshimanga',
    'author_email': 'bk.tshimanga@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
