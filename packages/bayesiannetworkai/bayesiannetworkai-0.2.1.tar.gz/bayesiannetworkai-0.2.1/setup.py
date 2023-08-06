# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bayesiannetworkai']

package_data = \
{'': ['*']}

install_requires = \
['pgmpy>=0.1.21,<0.2.0']

setup_kwargs = {
    'name': 'bayesiannetworkai',
    'version': '0.2.1',
    'description': 'A package for using Bayesian Networks',
    'long_description': '# bayesiannetworkai\n\nA package for using Bayesian Networks\n\n## Installation\n\n```bash\n$ pip install bayesiannetworkai\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`bayesiannetworkai` was created by GrupoAI. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`bayesiannetworkai` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'GrupoAI',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
