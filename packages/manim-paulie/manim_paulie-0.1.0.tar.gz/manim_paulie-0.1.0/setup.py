# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_paulie']

package_data = \
{'': ['*']}

install_requires = \
['manim>=0.3']

entry_points = \
{'manim.plugins': ['manim_paulie = manim_paulie']}

setup_kwargs = {
    'name': 'manim-paulie',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Pauline',
    'author_email': 'git@ethanlibs.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
