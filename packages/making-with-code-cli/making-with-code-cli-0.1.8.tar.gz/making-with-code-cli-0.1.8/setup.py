# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['making_with_code_cli', 'making_with_code_cli.git_backend']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.3,<9.0.0',
 'requests>=2.27.1,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['mwc = making_with_code_cli.cli:cli']}

setup_kwargs = {
    'name': 'making-with-code-cli',
    'version': '0.1.8',
    'description': 'Courseware for Making With Code',
    'long_description': "# Making With Code CLI\n\nThis package provides the command-line tool `mwc` which accompanies the Making With Code\nintroductory Computer Science curriculum. `mwc` helps students configure their computers, \nsets up git repositories for course assignemnts, and provides helpers for other course tasks\nlike running tests and accessing the curriculum.\n\nTeachers will be able to use `mwc` to adminster their courses, including tools for feedback and \nassessment. The overall goal of the project is to provide computational infrastructure to teachers\nand schools allowing them to teach CS through open-ended projects using real tools, supporting \npersonal relationships with powerful ideas and rich computing cultures. \n\n## Usage\n\n`mwc` can be installed via pip. However, if you're a student or teacher using \nMaking With Code, there is a separate bootstrapping process you should follow. \nPlease consult your curriculum website (or ask your teacher) for detailed instructions \non how and why to use this tool. \n\n    pip3 install making-with-code-cli\n\nOnce installed, you can set up your computer using the `mwc setup` command. Run \n`mwc --help` to see all the commands available.  \n\n## Contact\n\nIf you're interested in computing education and want to learn more about Making With Code, \nplease contact [Dr. Chris Proctor](https://chrisproctor.net).\n",
    'author': 'Chris Proctor',
    'author_email': 'chris@chrisproctor.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cproctor/making-with-code-courseware',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
