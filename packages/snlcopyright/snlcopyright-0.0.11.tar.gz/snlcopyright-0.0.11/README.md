# snlcopyright

Create, read, update, delete a copyright block in Python source code.

[![python](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/)
![os](https://img.shields.io/badge/os-ubuntu%20|%20macos%20|%20windows-blue.svg)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/sandialabs/snlcopyright#license) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![tests](https://github.com/sandialabs/snlcopyright/workflows/tests/badge.svg)](https://github.com/sandialabs/snlcopyright/actions) [![codecov](https://codecov.io/gh/sandialabs/snlcopyright/branch/main/graph/badge.svg)](https://codecov.io/gh/sandialabs/snlcopyright)

## Install

```bash
pip install snlcopyright
```

## Configure

*Optional:* Configure your local for [development](config/README.md).

## Use

```bash
copyright <path>
```

Examples:

```bash
copyright .  # process cwd and children

copyright ~/jdoe/foo  # process foo and children 
```

Command line entry points to the module are available via the `commands` command

```bash
commands

------------
snlcopyright
------------
This is the command line interface help for Sandia National Laboratories snlcopyright Python module.
Available commands:
commands           (this command)
copyright          Appends contents `copyright.txt` contents to .py files in the cwd, recursively.
copyright-info     Describes the installation details.
copyright-show     Echos the `copyright.txt` contents to the terminal.
copyright-status   Shows whether or not the copyright block was found in a .py file in the cwd, recursively.
copyright-version  Prints the semantic verison of the current installation.
```

## Contact

* Chad B. Hovey, Sandia National Laboratories, chovey@sandia.gov

## License

* [License](LICENSE)

Sandia National Laboratories is a multimission laboratory managed and operated by National Technology and Engineering Solutions of Sandia, LLC, a wholly owned subsidiary of Honeywell International, Inc., for the U.S. Department of Energy's National Nuclear Security Administration under contract DE-NA-0003525.

## Copyright

Copyright 2023 National Technology and Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

### Notice

For five (5) years from  the United States Government is granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable worldwide license in this data to reproduce, prepare derivative works, and perform publicly and display publicly, by or on behalf of the Government. There is provision for the possible extension of the term of this license. Subsequent to that period or any extension granted, the United States Government is granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable worldwide license in this data to reproduce, prepare derivative works, distribute copies to the public, perform publicly and display publicly, and to permit others to do so. The specific term of the license can be identified by inquiry made to National Technology and Engineering Solutions of Sandia, LLC or DOE.
 
NEITHER THE UNITED STATES GOVERNMENT, NOR THE UNITED STATES DEPARTMENT OF ENERGY, NOR NATIONAL TECHNOLOGY AND ENGINEERING SOLUTIONS OF SANDIA, LLC, NOR ANY OF THEIR EMPLOYEES, MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES ANY LEGAL RESPONSIBILITY FOR THE ACCURACY, COMPLETENESS, OR USEFULNESS OF ANY INFORMATION, APPARATUS, PRODUCT, OR PROCESS DISCLOSED, OR REPRESENTS THAT ITS USE WOULD NOT INFRINGE PRIVATELY OWNED RIGHTS.
 
Any licensee of this software has the obligation and responsibility to abide by the applicable export control laws, regulations, and general prohibitions relating to the export of technical data. Failure to obtain an export control license or other authority from the Government may result in criminal liability under U.S. laws.
