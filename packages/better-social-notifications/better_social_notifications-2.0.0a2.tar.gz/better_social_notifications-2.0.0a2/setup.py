# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['better_social_notifications',
 'better_social_notifications.helper',
 'better_social_notifications.notification',
 'better_social_notifications.youtube']

package_data = \
{'': ['*']}

install_requires = \
['apprise>=1.2.1,<2.0.0',
 'cachetools>=5.3.0,<6.0.0',
 'certifi>=2022.12.7,<2023.0.0',
 'charset-normalizer>=3.0.1,<4.0.0',
 'google-api-core>=2.11.0,<3.0.0',
 'google-api-python-client>=2.76.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth>=2.16.0,<3.0.0',
 'googleapis-common-protos>=1.58.0,<2.0.0',
 'httplib2>=0.21.0,<0.22.0',
 'idna>=3.4,<4.0',
 'isodate>=0.6.1,<0.7.0',
 'pip>=23.0,<24.0',
 'protobuf>=4.21.12,<5.0.0',
 'pyasn1-modules>=0.2.8,<0.3.0',
 'pyasn1>=0.4.8,<0.5.0',
 'pyparsing>=3.0.9,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2022.7.1,<2023.0.0',
 'requests>=2.28.2,<3.0.0',
 'rsa>=4.9,<5.0',
 'setuptools>=67.1.0,<68.0.0',
 'six>=1.16.0,<2.0.0',
 'tzlocal>=4.2,<5.0',
 'uritemplate>=4.1.1,<5.0.0',
 'urllib3>=1.26.14,<2.0.0',
 'wheel>=0.38.4,<0.39.0']

setup_kwargs = {
    'name': 'better-social-notifications',
    'version': '2.0.0a2',
    'description': '',
    'long_description': '',
    'author': 'Jack Stockley',
    'author_email': '34308937+jnstockley@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
