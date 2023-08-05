# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['async_shell']

package_data = \
{'': ['*']}

install_requires = \
['classlogging>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'async-shell',
    'version': '1.0.1',
    'description': 'Asyncio subprocess shell command wrapper',
    'long_description': '# async-shell\n\nAsyncio subprocess shell command wrapper.\n\n## Installation\n\n```shell\npip install async-shell\n```\n',
    'author': 'Artem Novikov',
    'author_email': 'artnew@list.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/reartnew/async-shell',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
