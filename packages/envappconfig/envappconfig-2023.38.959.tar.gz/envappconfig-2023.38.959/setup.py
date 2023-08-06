# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envappconfig']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'envappconfig',
    'version': '2023.38.959',
    'description': 'Simple app configuration via environment variables, in the spirit of argparse.',
    'long_description': '# envappconfig\n\nenvappconfig is intended to provide simple configuration via environment variables, in the same spirit as argparse, which can be useful when developing and deploying [12-factor apps](https://12factor.net).\n\nFeatures:\n* Autogenerates usage output if an environment variable is missing\n* Default settings for missing environment variables\n* Functions that transform the environment variable string to the value type you need\n* Environment variable prefixes\n\n## Basic example\n\n```python\nfrom envappconfig import EnvAppConfig\n\nenv = EnvAppConfig(description=\'Amazing app\')\nenv.add_env(\'port\', default=1234, transform=int, help=\'The listen port\')\nenv.add_env(\'mirror\', help=\'The URL to mirror\')\nconfig = env.configure()\n\n# Returns PORT from os.environ transformed to an int,\n# or 1234 if PORT does not exist.\nconfig.port\n\n# Returns MIRROR from os.environ,\n# or displays usage at env.configure()\n# if MIRROR does not exist, then exits.\nconfig.mirror\n```\n\n## Adding a prefix\n\nIf all the environment variables for the app have the same prefix, it can be specified with the `prefix` parameter.\n\n```python\nfrom envappconfig import EnvAppConfig\n\nenv = EnvAppConfig(prefix=\'MYAPP\', description=\'Amazing app\')\nenv.add_env(\'port\', default=1234, transform=int, help=\'The listen port\')\nenv.add_env(\'mirror\', help=\'The URL to mirror\')\nconfig = env.configure()\n\n# Returns MYAPP_PORT from os.environ transformed to an int,\n# or 1234 if MYAPP_PORT does not exist.\nconfig.port\n\n# Returns MYAPP_MIRROR from os.environ,\n# or displays usage at env.configure()\n# if MYAPP_MIRROR does not exist, then exits.\nconfig.mirror\n```\n\n## Custom transforms\n\nThe `transform` parameter can be used to specify normal transforms, like `int` or `float` (the default is `str`), but it can also take custom transform functions.  The transform function must take a single parameter, which will be filled in with the string value from the environment variable.\n\n```python\nenv = EnvAppConfig(description=\'Amazing app\')\n\n# Double the timeout specified in the TIMEOUT environment variable,\n# or default to 60.\nenv.add_env(\'timeout\', default=60, transform=lambda x: int(x) * 2, help=\'Timeout in seconds\')\n...\n```\n\n## Adding more config values\n\nAdditional config values can be added to an existing namespace, which can be helpful when there\'s a config value that needs to be calculated based on other config values.\n\n```python\nfrom envappconfig import EnvAppConfig\n\nenv = EnvAppConfig(description=\'Amazing app\')\nenv.add_env(\'bind\', help=\'IP address to bind to\')\nenv.add_env(\'port\', default=1234, transform=int, help=\'The listen port\')\nconfig = env.configure()\nconfig.listen = f\'{config.bind}:{config.port}\'\n\n# Returns the combined bind:port string.\nconfig.listen\n```\n\n## Command Line\n\nThere are a couple options for using envappconfig at the command line (eg. when testing).\n\n### Prefix\n\nIf you\'ve only got a couple environment variables to set, just put them before the command:\n\n```sh\nPORT=9999 NAME=foo python3 script_using_envappconfig.py\n```\n\n### dotenv\n\nIf you have more environment variables to set, consider using `dotenv`.  First put your environment variables in a file named `.env`:\n\n```sh\nPORT=9999\nNAME=foo\n```\n\nThen call `dotenv` as follows, which will load up the variables from `.env` for this command:\n\n```sh\ndotenv run -- python3 script_using_envappconfig.py\n```\n\nYou can install the `dotenv` command line tool with:\n\n```sh\npython3 -m pip install "python-dotenv[cli]"\n```\n',
    'author': 'Spectric Labs',
    'author_email': 'foss@spectric.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/spectriclabs/envappconfig',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
