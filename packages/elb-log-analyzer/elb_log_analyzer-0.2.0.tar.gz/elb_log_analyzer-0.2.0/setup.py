# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elb_log_analyzer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'elb-log-analyzer',
    'version': '0.2.0',
    'description': 'AWB ELB log analyzer',
    'long_description': "# ELB Log Analyzer\n\nTool for analyzing ELB logs for automating steps to retreive details of ip's user agent, total request count, to which urls requests were made along with their total count, and http methods in json format.\n\n## Installation\n\n- Using Pip\n\n    ```bash\n    python3 -m pip install elb-log-analyzer\n    ```\n\n## Usage\n\n- Print Help Menu\n\n    ```bash\n    python3 -m elb_log_analyzer -h\n    ```\n\n- Print json data on console\n\n    ```bash\n    python3 -m elb_log_analyzer -i [INPUT_LOG_FILE_PATH]\n    ```\n\n- Store json data in a file\n\n    ```bash\n    python3 -m elb_log_analyzer -i [INPUT_LOG_FILE_PATH] -o [OUTPUT_FILE_PATH]\n    ```\n\n    > **Note**: **INPUT_LOG_FILE_PATH** can be log file or a directory containing all log files ending with `.log` extension\n\n## Publish package to pypi\n\n- Using poetry\n\n    ```bash\n    python3 -m poetry publish --build --username [PYPI_USERNAME] --password [PYPI_PASSWORD]\n    ```\n",
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
