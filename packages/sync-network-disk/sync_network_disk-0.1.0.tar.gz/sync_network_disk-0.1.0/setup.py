# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sync_network_disk']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['snd = sync_network_disk.__main__:main']}

setup_kwargs = {
    'name': 'sync-network-disk',
    'version': '0.1.0',
    'description': '',
    'long_description': '1. 监控本地文件\n2. 监控云端文件',
    'author': 'jawide',
    'author_email': '596929059@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
