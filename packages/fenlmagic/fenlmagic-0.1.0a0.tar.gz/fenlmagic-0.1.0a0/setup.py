# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fenlmagic']

package_data = \
{'': ['*']}

install_requires = \
['kaskada>=0.1.0a0,<0.1.0']

setup_kwargs = {
    'name': 'fenlmagic',
    'version': '0.1.0a0',
    'description': '',
    'long_description': '',
    'author': 'Kevin J Nguyen',
    'author_email': 'kevin.nguyen@datastax.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
