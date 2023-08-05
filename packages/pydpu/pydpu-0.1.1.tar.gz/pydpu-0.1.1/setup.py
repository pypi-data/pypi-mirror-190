# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydpu']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydpu',
    'version': '0.1.1',
    'description': 'Python library and cli to communicate with DPUs and IPUs',
    'long_description': '# pydpu\n\n[![License](https://img.shields.io/github/license/opiproject/pydpu?style=flat&color=blue&label=License)](https://github.com/opiproject/pydpu/blob/main/LICENSE)\n[![Pulls](https://img.shields.io/docker/pulls/opiproject/pydpu.svg?logo=docker&style=flat&label=Pulls)](https://hub.docker.com/r/opiproject/pydpu)\n[![PyPI](https://img.shields.io/pypi/v/pydpu)](https://pypi.org/project/pydpu/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat)](https://github.com/psf/black)\n[![codecov](https://codecov.io/gh/opiproject/pydpu/branch/main/graph/badge.svg)](https://codecov.io/gh/opiproject/pydpu)\n[![Docker](https://github.com/opiproject/pydpu/actions/workflows/docker.yaml/badge.svg)](https://github.com/opiproject/pydpu/actions/workflows/docker.yaml)\n[![Tests](https://github.com/opiproject/pydpu/actions/workflows/test.yaml/badge.svg)](https://github.com/opiproject/pydpu/actions/workflows/test.yaml)\n\nPython library and cli to communicate with DPUs and IPUs\n\n## I Want To Contribute\n\nThis project welcomes contributions and suggestions.  We are happy to have the Community involved via submission of **Issues and Pull Requests** (with substantive content or even just fixes). We are hoping for the documents, test framework, etc. to become a community process with active engagement.  PRs can be reviewed by by any number of people, and a maintainer may accept.\n\nSee [CONTRIBUTING](https://github.com/opiproject/opi/blob/main/CONTRIBUTING.md) and [GitHub Basic Process](https://github.com/opiproject/opi/blob/main/doc-github-rules.md) for more details.\n',
    'author': 'OPI Dev',
    'author_email': 'opi-dev@lists.opiproject.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
