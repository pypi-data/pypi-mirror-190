# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pcluster_cli']

package_data = \
{'': ['*']}

install_requires = \
['aws-parallelcluster>=3.4.1,<4.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'sentry-sdk>=1.14.0,<2.0.0',
 'tabulate==0.8.10']

entry_points = \
{'console_scripts': ['pcl = pcluster_cli.main:main']}

setup_kwargs = {
    'name': 'pcluster-cli',
    'version': '0.1.2',
    'description': 'CLI for easy AWS parallel cluster management',
    'long_description': 'Usage\n======\n\n1. `pcl activate` - set default cluster\n\n2. `pcl create` - create parallel cluster\n\n3. `pcl delete` - delete parallel cluster\n\n4. `pcl list` - list aws parallel clusters\n\n5. `pcl add-queue` - add new slurm queue to the parallel cluster\n\n6. `pcl delete-queue` - remove existing slurm queue\n\n7. `pcl list-queues` - list existing slurm queues in a cluster\n\n8. `pcl s3-add` - mount s3 buckets in parallel cluster nodes\n\n9. `pcl s3-delete` - unmount s3 buckets in parallel cluster nodes\n\n10. `pcl ssh` - ssh/run a command inside parallel cluster head node\n\n11. `pcl save-ami` - save parallel cluster head node filesystem as ami\n  ',
    'author': 'rsingh',
    'author_email': 'rsingh@altoslabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
