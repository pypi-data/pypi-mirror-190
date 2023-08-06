# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nodeinfo']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'pynodeinfo',
    'version': '0.1.0',
    'description': 'Python Nodeinfo Library',
    'long_description': '# pynodeinfo\n\nPython NodeInfo library implemented with poetry.',
    'author': 'CSDUMMI',
    'author_email': 'csdummi.misquality@simplelogin.co',
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
