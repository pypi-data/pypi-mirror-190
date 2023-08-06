# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ecscmdb']

package_data = \
{'': ['*']}

install_requires = \
['ecspylibs==v1.1.15']

entry_points = \
{'console_scripts': ['cmdb = ecscmdb.cmdb:main',
                     'cmdbdiff = ecscmdb.cmdbdiff:main']}

setup_kwargs = {
    'name': 'ecscmdb',
    'version': '1.6.21',
    'description': 'Dump the OpenManage database.',
    'long_description': '# -*- coding: utf-8 -*-\n#\n# Do NOT edit this system file by hand -- use git.\n# See "URL to git source" below.\n#\n# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $\n#\n# Last Changed:  $Date: Wed Feb 8 18:51:00 2023 -0500 $\n#\n# URL to git source: $URL: git@git.wayne.edu:ECS_Projects/ECScmdb.git $\n#\n# ECScmdb\n\n cmdb: Download the devices in the OpenManage database into a spreadsheet, one work sheet for each device.\n\n cmdbdiff: Compare two cmdb spreadsheets for differences.\n\n## Installation\n\n Use Python virtual environment and install package ecscmdb.\n\n## Version\n\n # cmdb --version\n cmdb: ecscmdb(1.6.20), ecspylibs(1.1.14)\n\n # cmdbdiff --version\n cmdbdiff: ecscmdb(1.6.20), ecspylibs(1.1.14)\n\n## Help\n\n # cmdb --help\n\n Program to download the data from the OpenManage DB and build a spreadsheet.\n\n Some default option values listed below can be overridden within the\n configuration file.\n\n Usage:\n   cmdb [-v] [-L LEVEL] [--LOG=DIR] [-F] [-c CONFIG] [-s SECTION] [-o OUTPUT] [-p PWFILE] [-D] [-P SIZE]\n   cmdb [-vl] [-L LEVEL] [--LOG=DIR] [-c CONFIG] [-s SECTION] [-a ID]... [-d ID]... [-p PWFILE] [-D]\n   cmdb (-h | --help | -V | --version)\n\n   There are no required options.\n\n Options:\n   -h, --help                     Show this help message and exit.\n   -V, --version                  Show version information and exit.\n   -F, --full                     Show all data, no filtering.\n   -c CONFIG, --config=CONFIG     The configuration file.\n                                  Default: "/home/tom/Run/ECScmdb/Testing/etc/ecscmdb/cmdb.yml"\n   -s SECTION, --section=SECTION  The configuration file version (default\n                                  defined within the configuration file).\n   -o OUTPUT, --output=OUTPUT     Output file or directory.\n                                  Default: "/home/tom/Run/ECScmdb/Testing/output/OpenManage-cmdb.2023-02-08-18-14-30.xlsx"\n   -p PWFILE, --pw=PWFILE         The password file.  This file is used when a\n                                  login to a website or webpage is required.\n                                  Default: "/home/tom/Run/ECScmdb/Testing/etc/ecscmdb/cmdb.pw"\n   -l, --list                     List all of the IDs in the password file and\n                                  exit.  If both the --list and --verbose\n                                  options are included, list both IDs and\n                                  Passwords and exit.\n   -a ID, --add=ID                Add (or update) an ID and Password and exit.\n                                  Program will prompt for the Password to be\n                                  saved to the password file.\n   -d ID, --delete=ID             Delete an ID (if it exists) from the\n                                  password file and exit.\n   -v, --verbose                  Print verbose messages.\n   -L LEVEL, --log=LEVEL          Print log messages at log value LEVEL.\n                                  Valid levels are: TRACE, DEBUG, INFO, WARNING,\n                                  ERROR, and CRITICAL.\n                                  Default: WARNING\n   --LOG=DIR                      Log directory.\n                                  Default: "/home/tom/Run/ECScmdb/Testing/log/cmdb.log"\n   -D, --dryrun                   Only print out what would be done.\n   -P SIZE, --poolsize=SIZE       Call OpenManage using pools of size SIZE.\n                                  Default: set by the OS.\n\n # cmdbdiff --help\n\n Program to analyze two spreadsheets for differences.\n\n Some default option values listed below can be overridden within the initialization file.\n\n Usage:\n   cmdbdiff [-v] [-L LEVEL] [--LOG=DIR] [-c CONFIG] [-s SECTION] [-r REPORT] [-D] SPREADSHEET1 SPREADSHEET2\n   cmdbdiff (-h | --help | -V | --version)\n\n   Variables SPREADSHEET1 and SPREADSHEET2 are required, all other parameters are optional.\n\n Options:\n   -h, --help                          Show this help message and exit.\n   -V, --version                       Show version information and exit.\n   -c CONFIG, --config=CONFIG          The configuration file.\n                                       Default: "/home/tom/Run/ECScmdb/Testing/etc/ecscmdb/cmdbdiff.yml"\n   -s SECTION, --section=SECTION       The configuration file version (default\n                                       defined within the configuration file).\n   -r REPORT, --report=REPORT          Report directory or file.\n   -v, --verbose                       Print verbose messages.\n   -L LEVEL, --log=LEVEL               Print log messages at log value LEVEL.\n                                       Valid levels are: TRACE, DEBUG, INFO, WARNING,\n                                       ERROR, and CRITICAL.\n                                       Default: "WARNING"\n   --LOG=DIR                           Log Directory,\n                                       Default: "/home/tom/Run/ECScmdb/Testing/log/cmdbdiff.log"\n   -D, --dryrun                        Only print out what would be done.\n\n\n The GIT Home can be found [Here][CMDB].\n The README file can be found [Here][README].\n The LICENSE file can be found [Here][LICENSE].\n The ChangeLog file can be found [Here][CHANGELOG].\n The pyproject.toml file can be found [Here][PYPROJECT].\n My contact information can be found [Here][About Me].\n\n[CMDB]: https://git.wayne.edu/ECS_Projects/ECScmdb\n[README]: https://git.wayne.edu/ECS_Projects/ECScmdb/-/blob/master/README.md\n[LICENSE]: https://git.wayne.edu/ECS_Projects/ECScmdb/-/blob/master/LICENSE.txt\n[CHANGELOG]: https://git.wayne.edu/ECS_Projects/ECScmdb/-/blob/master/ChangeLog\n[PYPROJECT]: https://git.wayne.edu/ECS_Projects/ECScmdb/-/blob/master/pyproject.toml\n[About Me]: https://About.Me/Thomas.R.Stevenson\n',
    'author': 'Thomas R. Stevenson',
    'author_email': 'aa0026@wayne.edu',
    'maintainer': 'Thomas R. Stevenson',
    'maintainer_email': 'aa0026@wayne.edu',
    'url': 'https://git.wayne.edu/ECS_Projects/ECScmdb.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
