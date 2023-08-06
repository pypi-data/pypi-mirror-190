# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dolead_entry_points']

package_data = \
{'': ['*']}

install_requires = \
['celery>=3.1.17', 'requests>=2.13.0']

setup_kwargs = {
    'name': 'dolead-entry-points',
    'version': '0.0.8',
    'description': 'Multiple entry points generator',
    'long_description': '# Dolead Simple multi entry point lib\n',
    'author': 'François Schmidts',
    'author_email': 'francois@schmidts.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
