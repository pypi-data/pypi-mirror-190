# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mojap_airflow_tools']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow-providers-cncf-kubernetes==4.4.0', 'apache-airflow==2.4.3']

setup_kwargs = {
    'name': 'mojap-airflow-tools',
    'version': '2.4.3',
    'description': 'A few wrappers and tools to use Airflow on the Analytical Platform',
    'long_description': 'None',
    'author': 'MoJ Data Engineering',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
