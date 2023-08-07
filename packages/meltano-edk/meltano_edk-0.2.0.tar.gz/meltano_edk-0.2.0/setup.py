# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meltano', 'meltano.edk']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0.0,<7.0.0',
 'devtools>=0.9.0,<1',
 'pydantic>=1.9.0,<2',
 'structlog>=21,<22']

extras_require = \
{'docs': ['sphinx>=4.5,<6.0',
          'sphinx-rtd-theme>=0.5.2,<1.3.0',
          'sphinx-copybutton>=0.3.1,<0.6.0',
          'myst-parser>=0.17.2,<0.19.0',
          'sphinx-autobuild>=2021.3.14,<2022.0.0']}

setup_kwargs = {
    'name': 'meltano-edk',
    'version': '0.2.0',
    'description': 'A framework for building Meltano extensions',
    'long_description': "# Meltano extension developer kit\n\n[![Documentation Status](https://readthedocs.org/projects/meltano-edk/badge/?version=latest)](https://edk.meltano.com/en/latest/?badge=latest) |\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/meltano/edk/main.svg)](https://results.pre-commit.ci/latest/github/meltano/edk/main)\n\nThe Meltano extension developer kit is the fastest way to build custom Meltano extensions. If you're looking to build a custom extractor, loader, or tap then the [*SDK*](https://github.com/meltano/singer-sdk) is actually what you're looking for.\n\n## Creating a new extension using the EDK\n\nThis repo ships with a [copier](https://copier.readthedocs.io/en/stable/) based template to help developers get and new extension using the [Meltano EDK](https://edk.meltano.com) up and running quickly.\n\n### Prerequisites for using the template\n\nInstall copier:\n\n```bash\npipx install copier\n```\n\n### Use copier to initialize a new extension\n\nStart a new EDK project using the supplied template (directly from Github):\n\n```bash\ncopier gh:meltano/edk my-new-extension\n```\n\nInstall the project dependencies:\n\n```bash\ncd my-new-extension\npoetry install\n```\n\n## Developing extensions using the EDK\n\nFor detailed instructions on developing Meltano EDK extensions, see the [Meltano EDK documentation](https://edk.meltano.com) and review the [Work-In-Progress Specification](https://meltano-edk--28.org.readthedocs.build/en/28/specification.html).\n\nFor working examples of Meltano EDK extensions, see:\n\n- [dbt-ext](https://github.com/meltano/dbt-ext)\n- [cron-ext](https://github.com/meltano/cron-ext)\n",
    'author': 'Meltano Team and Contributors',
    'author_email': 'None',
    'maintainer': 'Meltano Team and Contributors',
    'maintainer_email': 'None',
    'url': 'https://meltano.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
