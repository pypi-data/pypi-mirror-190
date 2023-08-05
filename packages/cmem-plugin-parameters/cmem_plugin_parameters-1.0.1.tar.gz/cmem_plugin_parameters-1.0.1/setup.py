# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmem_plugin_parameters']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'cmem-plugin-base>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'cmem-plugin-parameters',
    'version': '1.0.1',
    'description': 'Set or overwrite parameters of a task.',
    'long_description': '# cmem-plugin-parameters\n\neccenca Corporate Memory Workflow plugin for parameter input\n\nThis is a plugin for [eccenca](https://eccenca.com) [Corporate Memory](https://documentation.eccenca.com).\n\nYou can install it with the [cmemc](https://eccenca.com/go/cmemc) command line\nclients like this:\n\n```\ncmemc admin workspace python install cmem-plugin-parameters\n```\n\n',
    'author': 'eccenca GmbH',
    'author_email': 'cmempy-developer@eccenca.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eccenca/cmem-plugin-parameters',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
