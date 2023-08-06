# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['applier']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=5.3.0,<6.0.0',
 'flask>=2.2.2,<3.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'salt>=3005.1,<3006.0']

setup_kwargs = {
    'name': 'applier',
    'version': '0.1.1',
    'description': 'Automatically apply SaltStack highstate on webhooks',
    'long_description': '# applier\n\nAutomatically apply SaltStack highstate on GitHub webhooks.\n\n\n### Configuration\n\nThe following environment variables can be configured:\n\n| Environment Variable       | Default        | Description                                                    |\n|----------------------------|----------------|----------------------------------------------------------------|\n| DEFAULT_BRANCH             | main           | The branch to perform updates on, typically the default branch |\n| SECRET_TTL                 | 900            | How many seconds to cache secrets for                          |\n| WEBHOOK_SECRET_SDB_KEY     | github-webhook | The SDB secret path to read from                               |\n| WEBHOOK_SECRET_SDB_BACKEND | secrets        | The SDB secret backend to use                                  |\n',
    'author': 'Alex Krantz',
    'author_email': 'alex@krantz.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
