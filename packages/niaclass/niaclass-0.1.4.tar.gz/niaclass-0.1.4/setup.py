# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niaclass']

package_data = \
{'': ['*']}

install_requires = \
['niapy>=2.0.4,<3.0.0',
 'numpy>=1.24.0,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'scikit-learn>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'niaclass',
    'version': '0.1.4',
    'description': 'Python framework for building classifiers using nature-inspired algorithms',
    'long_description': '<p align="center"><img src=".github/images/niaclass_logo.png" alt="NiaClass" title="NiaClass"/></p>\n\n---\n\n[![PyPI Version](https://img.shields.io/pypi/v/niaclass.svg)](https://pypi.python.org/pypi/niaclass)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/niaclass.svg)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/niaclass.svg)\n[![GitHub license](https://img.shields.io/github/license/lukapecnik/niaclass.svg)](https://github.com/lukapecnik/niaclass/blob/master/LICENSE)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/w/lukapecnik/niaclass.svg)\n[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/lukapecnik/niaclass.svg)](http://isitmaintained.com/project/lukapecnik/niaclass "Average time to resolve an issue")\n[![Percentage of issues still open](http://isitmaintained.com/badge/open/lukapecnik/niaclass.svg)](http://isitmaintained.com/project/lukapecnik/niaclass "Percentage of issues still open")\n![GitHub contributors](https://img.shields.io/github/contributors/lukapecnik/niaclass.svg)\n\nNiaClass is a framework for solving classification tasks using nature-inspired algorithms. The framework is written fully in Python. Its goal is to find the best possible set of classification rules for the input data using the <a href="https://github.com/NiaOrg/NiaPy">NiaPy framework</a>, which is a popular Python collection of nature-inspired algorithms. The NiaClass classifier supports numerical and categorical features.\n\n* **Free software:** MIT license,\n* **Documentation:** https://niaclass.readthedocs.io/en/latest/,\n* **Python versions:** 3.7.x, 3.8.x, 3.9.x.\n\n<p align="center"><img src=".github/images/niaclass.png" alt="NiaClass" title="NiaClass"/></p>\n\n## Installation\n\n### pip3\n\nInstall NiaClass with pip3:\n\n```sh\npip3 install niaclass\n```\n\nIn case you would like to try out the latest pre-release version of the framework, install it using:\n\n```sh\npip3 install niaclass --pre\n```\n\n### Fedora Linux\n\nTo install NiaClass on Fedora, use:\n\n```sh\n$ dnf install python-niaclass\n```\n\n## Functionalities\n\n- Binary classification,\n- Multi-class classification,\n- Support for numerical and categorical features.\n\n## Examples\n\nUsage examples can be found [here](examples).\n\n## Reference Papers (software is based on ideas from):\n\n[1] Iztok Fister Jr., Iztok Fister, Dušan Fister, Grega Vrbančič, Vili Podgorelec. [On the potential of the nature-inspired algorithms for pure binary classification](http://www.iztok-jr-fister.eu/static/publications/267.pdf). In. Computational science - ICCS 2020 : 20th International Conference, Proceedings. Part V. Cham: Springer, pp. 18-28. Lecture notes in computer science, 12141, 2020\n\n## Licence\n\nThis package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.\n\n## Disclaimer\n\nThis framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!\n\n## Cite us\n\nPečnik L., Fister I., Fister Jr. I. (2021) NiaClass: Building Rule-Based Classification Models Using Nature-Inspired Algorithms. In: Tan Y., Shi Y. (eds) Advances in Swarm Intelligence. ICSI 2021. Lecture Notes in Computer Science, vol 12690. Springer, Cham.\n\n',
    'author': 'Luka Pečnik',
    'author_email': 'lukapecnik96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lukapecnik/NiaClass',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
