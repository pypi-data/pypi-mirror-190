# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['byproxy', 'byproxy.proxy_checker', 'byproxy.proxy_maker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'byproxy',
    'version': '0.1.5',
    'description': 'ByProxy is a library to generate proxy dictionaries from a list of urls and gain information about the proxies.',
    'long_description': '# ByProxy\n\nByProxy is a simple package contains simple tools for proxy management and usage. You can generate proxy dictionaries from a list of urls and gain information about the proxies.\n\nCheck out the [byproxy API documentation](https://uykusuzdev.github.io/byproxy/) for more information.\n',
    'author': 'uykusuz',
    'author_email': 'vimevim@gmail.com',
    'maintainer': 'uykusuz',
    'maintainer_email': 'vimevim@gmail.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
