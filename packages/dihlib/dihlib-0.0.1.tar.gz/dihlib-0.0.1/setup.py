# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dihlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dihlib',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Example Package\n\nThis is a simple example package. You can use\n[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)\nto write your content.',
    'author': 'asdjakwd askdjö',
    'author_email': 'no@mail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
