# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plink_pipelines']

package_data = \
{'': ['*']}

install_requires = \
['aislib>=0.1.6-alpha.0,<0.2.0',
 'bed-reader>=0.2.24,<0.3.0',
 'deeplake>=3.0.13,<4.0.0',
 'luigi>=3.0.3,<4.0.0',
 'numpy==1.23.5',
 'pandas>=1.2.4,<2.0.0',
 'py>=1.10.0,<2.0.0']

entry_points = \
{'console_scripts': ['plink_pipelines = plink_pipelines.make_dataset:main']}

setup_kwargs = {
    'name': 'plink-pipelines',
    'version': '0.1.5a0',
    'description': '',
    'long_description': 'None',
    'author': 'Arnor Sigurdsson',
    'author_email': 'arnor-sigurdsson@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
