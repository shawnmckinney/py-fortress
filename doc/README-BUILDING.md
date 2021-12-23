# py-fortress README-BUILDING
-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Prerequisites
 * SECTION 2. Setup Python Runtime and Configure py-fortress Usage
___________________________________________________________________________________
## Document Overview

 * Contains instructions to build py-fortress
___________________________________________________________________________________
## SECTION 1. Prerequisites

Minimum hardware requirements:
 * 1 Core
 * 1 GB RAM

Minimum software requirements:
 * python-ldap dependencies installed [README-UPGRADE-PYTHON](./README-UPGRADE-PYTHON.md)
________________________________________________________________________________
## SECTION 2. Setup Python Runtime and Configure py-fortress Usage

1. Clone py-fortress
    ```
    git clone https://github.com/shawnmckinney/py-fortress.git
    ```

2. Change directory into root folder of project:
    ```
    cd py-fortress
    ```

3. Build

```bash
python3 -m venv env
. env/bin/activate
python3 -m pip install --upgrade build
python3 -m build
...
successfully built py-fortress-x.x.x.tar.gz and py_fortress-x.x.x-py3-none-any.wh
```

Where x.x.x == the current version of py-fortress

4. Install

```bash
pip install dist/py_fortress-x.x.x-py3-none-any.whl
```

Where x.x.x == the current version of py-fortress

#### End of # py-fortress README-BUILDING