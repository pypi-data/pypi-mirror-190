# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kyfkyf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kyfkyf',
    'version': '0.0.0',
    'description': 'A pure-Python Kafka clone',
    'long_description': "# Kyfkyf\n\nFor now I'm just squatting the name. If you need it for your project shoot me an email.\n",
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
