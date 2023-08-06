# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pybird']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pybird',
    'version': '1.2.0',
    'description': 'BIRD interface handler for Python',
    'long_description': '# pybird\n\n[![PyPI](https://img.shields.io/pypi/v/pybird.svg?maxAge=60)](https://pypi.python.org/pypi/pybird)\n[![PyPI](https://img.shields.io/pypi/pyversions/pybird.svg?maxAge=600)](https://pypi.python.org/pypi/pybird)\n[![Tests](https://github.com/20c/pybird/workflows/tests/badge.svg)](https://github.com/20c/confu)\n[![Codecov](https://img.shields.io/codecov/c/github/20c/pybird/main.svg?maxAge=3600)](https://codecov.io/github/20c/pybird)\n[![CodeQL](https://github.com/20c/pybird/actions/workflows/codeql.yml/badge.svg)](https://github.com/20c/pybird/actions/workflows/codeql.yml)\n\nBIRD interface handler for Python\n\nPyBird is a Python interface to the BIRD Internet Routing Daemon\'s UNIX control\nsocket, handling the socket connections and parsing the output. It was\noriginally written by [Sasha Romijn](https://github.com/mxsasha), forked from\nthe original BitBucket repository, and relicensed with permission.\n\n\nIn it\'s current state, you can use it to query the status of specific or all\nBGP peers, to query the routes received, accepted and rejected from a peer,\nor the general status of BIRD (router ID, last config change)\n\n\n# License\n\nCopyright 2016 20C, LLC\n\nCopyright 2011, Sasha Romijn <github@mxsasha.eu>\n\nAll rights reserved.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this softare except in compliance with the License.\nYou may obtain a copy of the License at\n\n   http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n',
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/20c/pybird',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
