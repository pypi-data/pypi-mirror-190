# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['json2csv']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=4.17.3,<5.0.0']

setup_kwargs = {
    'name': 'json-schema-to-csv',
    'version': '0.1.0',
    'description': '',
    'long_description': '# json schema to csv converter',
    'author': 'Łukasz Bacik',
    'author_email': 'mail@luka.sh',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
