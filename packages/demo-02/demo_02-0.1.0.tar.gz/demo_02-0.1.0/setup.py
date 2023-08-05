# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demo_02']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['demo = demo_02.main:app']}

setup_kwargs = {
    'name': 'demo-02',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Rizki Nur Barokah',
    'author_email': 'rizki@jkt1.ebdesk.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
