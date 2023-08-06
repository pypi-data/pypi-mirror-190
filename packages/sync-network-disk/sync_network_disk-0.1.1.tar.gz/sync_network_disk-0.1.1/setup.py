# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sync_network_disk']

package_data = \
{'': ['*']}

install_requires = \
['aligo>=5.5.13,<6.0.0',
 'configloaders>=0.3.2,<0.4.0',
 'flask>=2.2.2,<3.0.0',
 'watchdog>=2.2.1,<3.0.0']

entry_points = \
{'console_scripts': ['snd = sync_network_disk.__main__:main']}

setup_kwargs = {
    'name': 'sync-network-disk',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'jawide',
    'author_email': '596929059@qq.com',
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
