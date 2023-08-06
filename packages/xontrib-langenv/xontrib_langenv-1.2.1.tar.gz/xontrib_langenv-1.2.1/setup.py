# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xontrib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xontrib-langenv',
    'version': '1.2.1',
    'description': 'Pyenv/Nodenv/Goenv/Rbenv integration for xonsh',
    'long_description': '# xontrib-langenv\n\n[xonsh](https://xon.sh) integration with:\n\n* [Pyenv](https://github.com/pyenv/pyenv)\n* [Nodenv](https://github.com/nodenv/nodenv)\n* [Goenv](https://github.com/syndbg/goenv)\n* [Rbenv](https://github.com/rbenv/rbenv)\n\nThis xontrib replaces the slow `langenv` initialization with a faster python version (and skips the `rehash` step), which could save up to ~0.5s for each `lang`\n\nThe only two exceptions are:\n\n  - `goenv`, which requires an extra `rehash --only-manage-paths` [init step](https://github.com/syndbg/goenv/blob/e1007619dbb180c8f8032a9dcdb7afbeb88e848a/libexec/goenv-init#L167) to set some more [environment variables](https://github.com/syndbg/goenv/blob/e1007619dbb180c8f8032a9dcdb7afbeb88e848a/libexec/goenv-sh-rehash#L24)\n  - `virtualenv-init`\n\nso if you rewrite that `goenv` env var setting and `pyenv` `virtualenv` init logic in python and xontribute to this xontrib, you could eliminate the last sources of xonsh langenv startup delay!\n\n## Install\n\nInstall using pip\n\n```\npip install xontrib-langenv\n```\n\n## Usage\n\nAdd to your `.xonshrc` as follows:\n\n### Pyenv\n\n```sh\nxontrib load pyenv\n```\n\nThis xontrib initializes `pyenv` when `xonsh` is started.\nAfter initialization `pyenv` commands works as they would do in any *classic* shell.\n\nAlso supports [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).\n\n### Nodenv\n\n```sh\nxontrib load nodenv\n```\n\nThis xontrib initializes `nodenv` when `xonsh` is started.\nAfter initialization `nodenv` commands works as they would do in any *classic* shell.\n\n### Goenv\n\n```sh\nxontrib load goenv\n```\n\nThis xontrib initializes `goenv` when `xonsh` is started.\nAfter initialization `goenv` commands works as they would do in any *classic* shell.\n\n### Rbenv\n\n```sh\nxontrib load rbenv\n```\n\nThis xontrib initializes `rbenv` when `xonsh` is started.\nAfter initialization `rbenv` commands works as they would do in any *classic* shell.\n\n## Compatibility notes\n\nIf you are using `xonsh` v0.11 (or older) and you have issues with the latest version of this xontrib, try to downgrade it to version 1.0.6.\n',
    'author': 'Gyuri Horak',
    'author_email': 'dyuri@horak.hu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dyuri/xontrib-langenv',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
