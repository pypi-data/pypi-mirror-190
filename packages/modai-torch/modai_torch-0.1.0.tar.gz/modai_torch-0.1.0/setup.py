# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['modai_torch']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0,<23.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'setuptools>=65.6.3,<66.0.0',
 'typer[all]>=0.7.0,<0.8.0',
 'wheel>=0.38.4,<0.39.0']

extras_require = \
{'all': ['autoflake>=1.4,<2.0',
         'black>=22.3.0,<23.0.0',
         'isort>=5.12.0,<6.0.0',
         'mkdocs>=1.4.2,<2.0.0',
         'mkdocs-material>=8.5.11,<9.0.0',
         'mkdocs-material-extensions>=1.1.1,<2.0.0',
         'mkdocs-macros-plugin>=0.7.0,<0.8.0',
         'mkdocstrings[python]>=0.20.0,<0.21.0',
         'mypy>=0.961,<0.962',
         'pytest>=7.2.0,<8.0.0',
         'pytest-vscodedebug>=0.1.0,<0.2.0',
         'pyupgrade>=2.37.3,<3.0.0',
         'xdoctest[all]>=1.1.0,<2.0.0'],
 'test': ['autoflake>=1.4,<2.0',
          'black>=22.3.0,<23.0.0',
          'isort>=5.12.0,<6.0.0',
          'mkdocs>=1.4.2,<2.0.0',
          'mkdocs-material>=8.5.11,<9.0.0',
          'mkdocs-material-extensions>=1.1.1,<2.0.0',
          'mkdocs-macros-plugin>=0.7.0,<0.8.0',
          'mkdocstrings[python]>=0.20.0,<0.21.0',
          'mypy>=0.961,<0.962',
          'pytest>=7.2.0,<8.0.0',
          'pytest-vscodedebug>=0.1.0,<0.2.0',
          'pyupgrade>=2.37.3,<3.0.0',
          'xdoctest[all]>=1.1.0,<2.0.0']}

setup_kwargs = {
    'name': 'modai-torch',
    'version': '0.1.0',
    'description': 'A modular library for building AI models in PyTorch',
    'long_description': '# ModAI Torch\n\nA modular library for building AI applications using PyTorch.\n\n## Installation\n\n`pip install modai_torch`\n',
    'author': 'Aditya Gudimella',
    'author_email': 'aditya.gudimella@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
