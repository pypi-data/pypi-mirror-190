# -*- coding: utf-8 -*-
#
# Do NOT edit this system file by hand -- use git.
# See "URL to git source" below.
#
# Author:        $Id: Thomas R. Stevenson <aa0026@wayne.edu> $
#
# Last Changed:  $Date: Thu Jan 19 16:19:24 2023 -0500 $
#
# URL to git source: $URL: git@git.wayne.edu:aa0026/cmdb.git $
#
# cmdb

cmdb: Download the devices in the OpenManage database into a spreadsheet, one work sheet for each device.

cmdbdiff: Compare two cmdb spreadsheets for differences.

## Installation

Use Python virtual environment and install package cmdb.

## Usage

cmdb --help

```
Program to download the data from the OpenManage DB and build a spreadsheet.

Some default option values listed below can be overridden within the
configuration file.

Usage:
  cmdb [-v] [-L LEVEL] [--LOG=DIR] [-F] [-c CONFIG] [-s SECTION] [-o OUTPUT] [-p PWFILE] [-D] [-P SIZE]
  cmdb [-vl] [-L LEVEL] [--LOG=DIR] [-c CONFIG] [-s SECTION] [-a ID]... [-d ID]... [-p PWFILE] [-D]
  cmdb (-h | --help | -V | --version)

  There are no required options.

Options:
  -h, --help                     Show this help message and exit.
  -V, --version                  Show version information and exit.
  -F, --full                     Show all data, no filtering.
  -c CONFIG, --config=CONFIG     The configuration file.
                                 Default: "/home/tom/Run/ECScmdb/Poetry/etc/ecscmdb/cmdb.yml"
  -s SECTION, --section=SECTION  The configuration file version (default
                                 defined within the configuration file).
  -o OUTPUT, --output=OUTPUT     Output file or directory.
                                 Default: "/home/tom/Run/ECScmdb/Poetry/output/OpenManage-cmdb.2023-01-19-16-14-32.xlsx"
  -p PWFILE, --pw=PWFILE         The password file.  This file is used when a
                                 login to a website or webpage is required.
                                 Default: "/home/tom/Run/ECScmdb/Poetry/etc/ecscmdb/cmdb.pw"
  -l, --list                     List all of the IDs in the password file and
                                 exit.  If both the --list and --verbose
                                 options are included, list both IDs and
                                 Passwords and exit.
  -a ID, --add=ID                Add (or update) an ID and Password and exit.
                                 Program will prompt for the Password to be
                                 saved to the password file.
  -d ID, --delete=ID             Delete an ID (if it exists) from the
                                 password file and exit.
  -v, --verbose                  Print verbose messages.
  -L LEVEL, --log=LEVEL          Print log messages at log value LEVEL.
                                 Valid levels are: TRACE, DEBUG, INFO, WARNING,
                                 ERROR, and CRITICAL.
                                 Default: WARNING
  --LOG=DIR                      Log directory.
                                 Default: "/home/tom/Run/ECScmdb/Poetry/log/cmdb.log"
  -D, --dryrun                   Only print out what would be done.
  -P SIZE, --poolsize=SIZE       Call OpenManage using pools of size SIZE.
                                 Default: set by the OS.
```

cmdbdiff --help

```
Program to analyze two spreadsheets for differences.

Some default option values listed below can be overridden within the initialization file.

Usage:
  cmdbdiff [-v] [-L LEVEL] [--LOG=DIR] [-c CONFIG] [-s SECTION] [-r REPORT] [-D] SPREADSHEET1 SPREADSHEET2
  cmdbdiff (-h | --help | -V | --version)

  Variables SPREADSHEET1 and SPREADSHEET2 are required, all other parameters are optional.

Options:
  -h, --help                          Show this help message and exit.
  -V, --version                       Show version information and exit.
  -c CONFIG, --config=CONFIG          The configuration file.
                                      Default: "/home/tom/Run/ECScmdb/Poetry/etc/ecscmdb/cmdbdiff.yml"
  -s SECTION, --section=SECTION       The configuration file version (default
                                      defined within the configuration file).
  -r REPORT, --report=REPORT          Report directory or file.
  -v, --verbose                       Print verbose messages.
  -L LEVEL, --log=LEVEL               Print log messages at log value LEVEL.
                                      Valid levels are: TRACE, DEBUG, INFO, WARNING,
                                      ERROR, and CRITICAL.
                                      Default: "WARNING"
  --LOG=DIR                           Log Directory,
                                      Default: "/home/tom/Run/ECScmdb/Poetry/log/cmdbdiff.log"
  -D, --dryrun                        Only print out what would be done.
```

## Documentation
Program to analyze two spreadsheets for differences.

Some default option values listed below can be overridden within the initialization file.

Usage:
  cmdbdiff [-v] [-L LEVEL] [--LOG=DIR] [-c CONFIG] [-s SECTION] [-r REPORT] [-D] SPREADSHEET1 SPREADSHEET2
  cmdbdiff (-h | --help | -V | --version)

  Variables SPREADSHEET1 and SPREADSHEET2 are required, all other parameters are optional.

Options:
  -h, --help                          Show this help message and exit.
  -V, --version                       Show version information and exit.
  -c CONFIG, --config=CONFIG          The configuration file.
                                      Default: "/home/tom/Run/ECScmdb/Poetry/etc/ecscmdb/cmdbdiff.yml"
  -s SECTION, --section=SECTION       The configuration file version (default
                                      defined within the configuration file).
  -r REPORT, --report=REPORT          Report directory or file.
  -v, --verbose                       Print verbose messages.
  -L LEVEL, --log=LEVEL               Print log messages at log value LEVEL.
                                      Valid levels are: TRACE, DEBUG, INFO, WARNING,
                                      ERROR, and CRITICAL.
                                      Default: "WARNING"
  --LOG=DIR                           Log Directory,
                                      Default: "/home/tom/Run/ECScmdb/Poetry/log/cmdbdiff.log"
  -D, --dryrun                        Only print out what would be done.

The GIT Home can be found [Here][CMDB].
The README file can be found [Here][README].
The LICENSE file can be found [Here][LICENSE].
The ChangeLog file can be found [Here][CHANGELOG].
The pyproject.toml file can be found [Here][PYPROJECT].
My contact information can be found [Here][About Me].

[CMDB]: https://git.wayne.edu/aa0026/cmdb
[README]: https://git.wayne.edu/aa0026/cmdb/-/blob/master/README.md
[LICENSE]: https://git.wayne.edu/aa0026/cmdb/-/blob/master/LICENSE.txt
[CHANGELOG]: https://git.wayne.edu/aa0026/cmdb/-/blob/master/ChangeLog
[PYPROJECT]: https://git.wayne.edu/aa0026/cmdb/-/blob/master/pyproject.toml
[About Me]: https://About.Me/Thomas.R.Stevenson
