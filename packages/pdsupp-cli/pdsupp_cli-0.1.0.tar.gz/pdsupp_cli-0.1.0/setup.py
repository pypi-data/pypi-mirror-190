# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pdsupp_cli']

package_data = \
{'': ['*']}

install_requires = \
['gracy>=1.6.0,<2.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pspdbeta = pdsupp_cli.commands:app']}

setup_kwargs = {
    'name': 'pdsupp-cli',
    'version': '0.1.0',
    'description': '(pre-release) PagerDuty Public Support Scripts CLI App',
    'long_description': '\n[![CircleCI](https://dl.circleci.com/status-badge/img/gh/PagerDuty/pdsupp_cli/tree/main.svg?style=svg&circle-token=8eba9a14bddce13134d9dac56397a8ef2506dd60)](https://dl.circleci.com/status-badge/redirect/gh/PagerDuty/pdsupp_cli/tree/main)\n\n# [Automatic Dev Docs](https://probable-fiesta-292lyp2.pages.github.io/pdsupp_cli.html)\n\n# Installation & Use (note: **Pre-Release**)\nInstall:\n```bash\npip install pdsupp_cli\n```\n\nUse:\n```bash\npspdbeta --help\n```\n\n# Goal:\n\n## 1\nMove the hard work represented in [PagerDuty Public Support Scripts](https://github.com/PagerDuty/public-support-scripts) to an accessible, user-friendly, but low-maintenance CLI framework.\n\nOffer basic help, parsing, and a `pip install ...` option for users.\n\n## 2\nAdd unit and integration tests to the varous script conversions to make extension and maintenance feel (and *be*) safer!\n\n## 3 \nAdd developer documentation (alongside auto-doc publication and in-IDE registration) to the scripts to make maintenance and extension (and inspiration) more fun and efficient!\n\n## 4\nOffer a learning project to share with anyone who wants to work with CLI apps, small-scale automated CI/CD processes, and modern Python idioms.\n\n\n# General Repo characteristics:\n\n## Python Skeleton Repo\nThis repo is derived from an in-progress [Python+Poetry Skeleton](https://github.com/ethanmsl/skelly-explorer).  All code there is functional.  However some knowledge of what variables to populate is still required.\n\n## Supported Virtual Environoment, Dependency, and Publication Mgmgt Environment:\nThis repo is designed for use with the [Poetry](https://python-poetry.org/) environment.\nThe code it runs assumes that .venv\'s are local.\nSet with:\n```bash\npoetry config virtualenvs.in-project true\n```\n\nCheck with:\n```bash\npoetry config --list\n```\n\nThe repo also uses pre-commit hooks (download separately, as `.git/` is not automatically synched) that auto-populate a `requirements.txt` & `requirements-dev.txt` so Poetry is **NOT** required for building and exploration.  (However the CI/CD scripts will use the Poetry system.)\n\n## Dev-Dependencies Specified\n- formatting: `isort` & `black`\n- linting: `pylint`\n- lsp & typechecking: `pyright`\n- testing: `pytest` + `coverage` (via `pytest-cov`)\n- auto-documentation: `pdoc` (*not* ~~"pdoc3"~~, which should be strongly avoided)\n\n\n## Run Pre-Commit Hook Manually\nfrom anywhere in project:\n```zsh\ngit hook run pre-commit\n```\n\n## Note:\nDue to runner environment caching in GitHub Workflow environment renaming needs to be accompanied by explicit cache deletion.  And possible other maintenance.\n',
    'author': 'Ethan Skowronski-Lutz',
    'author_email': '33399972+ethanmsl@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
