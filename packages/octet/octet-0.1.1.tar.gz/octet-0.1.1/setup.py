# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['octet']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'octet',
    'version': '0.1.1',
    'description': 'Object-oriented way to represent digital sizes (bits and bytes)',
    'long_description': '# octet\n\nObject-oriented way to represent digital sizes (bits and bytes)\n\n## Examples\n\n```python\n>>> from octet import *\n>>> GiB(1024).convert_to(TiB)\nTebiByte(1)\n>>> size = 1024 * KiB()\n>>> size.to_minor_units()\nbit(8388608)\n>>> KiB(1) > 1000 * B()\nTrue\n>>> KiB(1) > 1025 * B()\nFalse\n```\n',
    'author': 'Enrique Soria',
    'author_email': 'me@enriquesoria.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/EnriqueSoria/octet',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
