# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acrclient']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2']

setup_kwargs = {
    'name': 'acrclient',
    'version': '0.1.1',
    'description': 'API wrapper for the v2 ACRCloud API.',
    'long_description': '# Python ACR Client module\n\nContains a simple client for calling the v2 endpoints of the [ACRCloud](https://www.acrcloud.com) API.\n\n## Installation\n\n```bash\npoetry add acrclient\n\n# or on old setup style projects\npip -m install acrclient\n```\n\n## Usage\n\n```python\n>>> from acrclient import Client\n>>> client = Client(bearer_token="bearer-token")\n\n```\n\n## Development\n\n```bash\n# setup a dev env\npython -mvenv env\n. env/bin/activate\n\n# install a modern poetry version\npython -mpip install poetry>=1.2.0\n\n# install deps and dev version\npoetry install\n\n# make changes, run tests\npoetry run pytest\n```\n\n## Release Management\n\nThe CI/CD setup uses semantic commit messages following the [conventional commits standard](https://www.conventionalcommits.org/en/v1.0.0/).\nThere is a GitHub Action in [.github/workflows/semantic-release.yaml](./.github/workflows/semantic-release.yaml)\nthat uses [go-semantic-commit](https://go-semantic-release.xyz/) to create new\nreleases.\n\nThe commit message should be structured as follows:\n\n```\n<type>[optional scope]: <description>\n\n[optional body]\n\n[optional footer(s)]\n```\n\nThe commit contains the following structural elements, to communicate intent to the consumers of your library:\n\n1. **fix:** a commit of the type `fix` patches gets released with a PATCH version bump\n1. **feat:** a commit of the type `feat` gets released as a MINOR version bump\n1. **BREAKING CHANGE:** a commit that has a footer `BREAKING CHANGE:` gets released as a MAJOR version bump\n1. types other than `fix:` and `feat:` are allowed and don\'t trigger a release\n\nIf a commit does not contain a conventional commit style message you can fix\nit during the squash and merge operation on the PR.\n\nOnce a commit has landed on the `main` branch a release will be created and automatically published to [pypi](https://pypi.org/)\nusing the GitHub Action in [.github/workflows/release.yaml](./.github/workflows/release.yaml) which uses [poetry](https://python-poetry.org/)\nto publish the package to pypi.\n\n## License\n\nThis package is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, version 3 of the License.\n\n## Copyright\n\nCopyright (c) 2023 [Radio Bern RaBe](http://www.rabe.ch)\n',
    'author': 'RaBe IT-Reaktion',
    'author_email': 'it@rabe.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
