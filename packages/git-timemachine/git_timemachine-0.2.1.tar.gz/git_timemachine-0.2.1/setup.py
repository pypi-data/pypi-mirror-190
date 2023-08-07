# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['git_timemachine', 'git_timemachine.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['git-timemachine = git_timemachine.__main__:cli']}

setup_kwargs = {
    'name': 'git-timemachine',
    'version': '0.2.1',
    'description': 'A command-line tool to help you manage Git commits at different time nodes.',
    'long_description': "# git-timemachine\n\nA command-line tool to help you manage Git commits at different time nodes.\n\n## Quickstart\n\n1. Install command-line tool `git-timemachine` via command:\n\n    ```shell\n    pip install git-timemachine\n    ```\n\n2. Initialize configurations for `git-timemachine`:\n\n    ```shell\n    git-timemachine config --init\n    ```\n\n3. Edit the timestamp for last commit and range of time growth\n   in `$HOME/.git-timemachine/config` by any plain text editor.\n\n4. In a Git repository, run the following command to record a commit according\n   to the timestamp in configurations:\n\n    ```shell\n   git-timemachine commit -m 'A commit from specified time point.'\n    ```\n\n5. Grow the timestamp for next commits:\n    ```shell\n   git-timemachine grow\n    ```\n\n## License\n\nCopyright (C) 2022 HE Yaowen <he.yaowen@hotmail.com>\n\nThe GNU General Public License (GPL) version 3, see [LICENSE](./LICENSE).\n",
    'author': 'HE Yaowen',
    'author_email': 'he.yaowen@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/he-yaowen/git-timemachine',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
