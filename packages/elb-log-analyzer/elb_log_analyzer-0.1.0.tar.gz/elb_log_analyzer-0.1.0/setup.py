# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elb_log_analyzer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'elb-log-analyzer',
    'version': '0.1.0',
    'description': 'AWB ELB log analyzer',
    'long_description': '',
    'author': 'Dhrumil Mistry',
    'author_email': '56185972+dmdhrumilmistry@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
