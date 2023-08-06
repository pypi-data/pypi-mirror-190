# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tapshex']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'black>=22.12.0,<23.0.0',
 'click>=8.1.3,<9.0.0',
 'dctap>=0.4.4,<0.5.0',
 'ipdb>=0.13.11,<0.14.0',
 'ipykernel>=6.20.1,<7.0.0',
 'ipython==8.8.0',
 'jinja2-cli>=0.8.2,<0.9.0',
 'pip-tools>=6.12.1,<7.0.0',
 'pre-commit>=2.21.0,<3.0.0',
 'pyshexc>=0.9.1,<0.10.0']

setup_kwargs = {
    'name': 'tapshex',
    'version': '0.2.3',
    'description': 'Converts TAP/CSV into ShEx Schema',
    'long_description': 'tapshex\n=======\n\nGenerate ShEx from tabular application profiles in DCTAP format.\n',
    'author': 'Tom Baker',
    'author_email': 'tom@tombaker.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/tapshex/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
