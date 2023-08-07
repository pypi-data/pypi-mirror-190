# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pympistandard', 'pympistandard.data']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pympistandard',
    'version': '0.1.1',
    'description': 'Python API to the MPI Standard',
    'long_description': 'None',
    'author': 'Martin Ruefenacht',
    'author_email': 'martin.ruefenacht@lrz.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
