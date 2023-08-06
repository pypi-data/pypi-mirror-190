# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tutorial_hypermodern_python_winand']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'desert>=2022.9.22,<2023.0.0',
 'marshmallow>=3.19.0,<4.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-python = '
                     'tutorial_hypermodern_python_winand.console:main']}

setup_kwargs = {
    'name': 'tutorial-hypermodern-python-winand',
    'version': '0.1.0',
    'description': 'The hypermodern Python project',
    'long_description': '# tutorial-hypermodern-python-winand\n[![Tests](https://github.com/Winand/tutorial-hypermodern-python-winand/workflows/Tests/badge.svg)](https://github.com/Winand/tutorial-hypermodern-python-winand/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/Winand/tutorial-hypermodern-python-winand/branch/master/graph/badge.svg)](https://codecov.io/gh/Winand/tutorial-hypermodern-python-winand)\n\nHypermodern Python tutorial series\n\n## Links\n* https://cjolowicz.github.io/posts/hypermodern-python-01-setup\n* https://github.com/cjolowicz/hypermodern-python\n* https://winand.notion.site/Hypermodern-Python-38cf6036f64447a19d527293de373415 (ru)\n',
    'author': 'Makarov Andrey',
    'author_email': 'winandfx@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Winand/tutorial-hypermodern-python-winand',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
