# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tailk']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'rich>=13.2.0,<14.0.0', 'uvloop>=0.17.0,<0.18.0']

entry_points = \
{'console_scripts': ['tailk = tailk.main:main']}

setup_kwargs = {
    'name': 'tailk',
    'version': '0.1.0',
    'description': 'Tail kubernetes pods logs',
    'long_description': '# TailK\n\n![pyversions](https://img.shields.io/pypi/pyversions/tailk.svg) [![PyPi Status](https://img.shields.io/pypi/v/tailk.svg)](https://pypi.org/project/tailk/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/tailk) ![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ffaraone/tailk/test.yml?branch=master) ![Codecov](https://img.shields.io/codecov/c/github/ffaraone/tailk)\n\n## Introduction\n\n`TaikK` is a small utility to tail logs from multiple Kubernetes pods.\n\n## Installation\n\n`TailK` requires Python 3.8+ and `kubectl` available in your shell.\n\n### Using pip\n\n```\n$ pip install tailk\n```\n\n### Using Homebrew\n\n```\n$ brew update\n$ brew tap ffaraone/birre\n$ brew install ffaraone/birre/tailk\n```\n\n\n## Usage\n\n### Basic usage\n\n```\n$ tailk pattern1 [...]\n```\n\nwhere `pattern1` is any valid Python regular expression.\n\n> Multiple patterns are combined with a logical `OR`.\n\n\n### Advanced usage\n\nYou may want to highlight portions of the log. In this case you can provide highlighting patterns in the following way:\n\n```\n$ tailk pattern1 --highlight hl-pattern-1 [--highlight hl-pattern-2]\n```\n\nwhere `hl-pattern-1` is any valid Python regular expression.\n\nYou can also customize the style for highlight. In this case your patterns must be specified using named capturing groups\n\n```\n$ tailk pattern1 --highlight "(?P<hello>HELLO)" --style "hello:underline magenta"\n```\n\n## License\n\n`TailK` is released under the [Apache License Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).\n',
    'author': 'Francesco Faraone',
    'author_email': 'ffaraone@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ffaraone/tailk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
