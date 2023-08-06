# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eagerx_franka',
 'eagerx_franka.franka_arm',
 'eagerx_franka.franka_arm.pybullet',
 'eagerx_franka.ik',
 'eagerx_franka.solid',
 'eagerx_franka.solid.assets']

package_data = \
{'': ['*']}

install_requires = \
['eagerx-pybullet>=0.1.11,<0.2.0',
 'eagerx-utility>=0.0.2,<0.0.3',
 'eagerx>=0.1.33,<0.2.0',
 'modern-robotics>=1.1.0,<2.0.0',
 'moviepy>=1.0.3,<2.0.0',
 'numpy<1.20.0',
 'roboticstoolbox-python>=1.0.3,<2.0.0',
 'stable-baselines3>=1.6.2,<2.0.0',
 'tensorboard>=2.11.0,<3.0.0',
 'urdf-parser-py>=0.0.4,<0.0.5']

setup_kwargs = {
    'name': 'eagerx-franka',
    'version': '0.0.3',
    'description': 'EAGERx interface to franka robot arms.',
    'long_description': 'None',
    'author': 'Jelle Luijkx',
    'author_email': 'j.d.luijkx@tudelft.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eager-dev/eagerx_franka',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
