# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bmt']

package_data = \
{'': ['*']}

install_requires = \
['deprecation>=2.1.0,<3.0.0',
 'linkml-runtime>=1.4,<2.0',
 'oaklib>=0.1.71,<0.2.0',
 'pytest>=7.2.0,<8.0.0',
 'recommonmark>=0.7.1,<0.8.0',
 'sphinx-autodoc-typehints>=1.19.5,<2.0.0',
 'sphinx-click>=4.3.0,<5.0.0',
 'sphinx-rtd-theme>=1.1.1,<2.0.0',
 'sphinxcontrib-napoleon>=0.7,<0.8',
 'stringcase>=1.2.0,<2.0.0',
 'twine>=4.0.1,<5.0.0']

extras_require = \
{':extra == "docs"': ['Sphinx>=5.3.0,<6.0.0']}

setup_kwargs = {
    'name': 'bmt',
    'version': '1.0.1',
    'description': 'Biolink Model Toolkit: A Python API for working with the Biolink Model',
    'long_description': '[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)]()\n[![PyPI](https://img.shields.io/pypi/v/bmt)](https://img.shields.io/pypi/v/bmt)\n\n# Biolink Model Toolkit\n\nBiolink Model Toolkit (BMT): A Python API for working with the [Biolink Model](https://github.com/biolink/biolink-model).\n\nBMT provides utility functions to look up Biolink Model for classes, relations, and properties based on Biolink CURIEs\nor external CURIEs that have been mapped to Biolink Model.\n\n> Note: Each release of BMT is pinned to a specific version of the Biolink Model to ensure consistency.\n\n## Usage\n\nBMT provides convenience methods to operate on the Biolink Model.\n\nUsing this toolkit you can,\n- Get Biolink Model elements corresponding to a given Biolink class or slot name\n- Get Biolink Model elements corresponding to a given external CURIE/IRI\n- Get ancestors for a given Biolink Model element\n- Get descendants for a given Biolink Model element\n- Get parent for a given Biolink Model element\n- Get children for a given Biolink Model element\n- Check whether a given Biolink Model element is part of a specified subset',
    'author': 'Sierra Taylor Moxon',
    'author_email': 'sierra.taylor@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/biolink/biolink-model-toolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
