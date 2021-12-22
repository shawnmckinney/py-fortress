# py-fortress DEVELOPERS GUIDE
-------------------------------------------------------------------------------

## Table of Contents

 * Document Overview
 * SECTION 1. Prerequisites
 * SECTION 2. Env Prep & Build
 * SECTION 3. Promote to TESTPYPI and Test
 * SECTION 4. Tag the release
 * SECTION 5. Promote to PYPI
___________________________________________________________________________________
## Document Overview

Instructions to release py-fortress package
___________________________________________________________________________________
## SECTION 1. Prerequisites

Minimum hardware requirements:
 * 1 Core
 * 1 GB RAM

Prerequisites:
 * Linux machine with Internet connection
 * Python3
 * Accounts setup on testpypi and pypi with access to py-fortress project
 * Account setup on github with contributor access to py-fortress

________________________________________________________________________________
## SECTION 2. Env Prep & Build

1. Clone the project
```bash
git clone https://github.com/shawnmckinney/py-fortress.git
```

2. Prepare the virutal env:
```bash
python3 -m venv env
. env/bin/activate
python3 -m pip install --upgrade build
```

3. Build:
```bash
python3 -m build
```
________________________________________________________________________________
## SECTION 3. Promote to TESTPYPI and Test

1. Setup twine:
```bash
pip install --upgrade twine 
```

2. Push the package to testpypi:
```bash
python3 -m twine upload --repository testpypi dist/*
```

3. Install to test machine
```bash
pip install --index-url https://test.pypi.org/py-fortress/ --no-deps YOUR-USERNAME-HERE
```

* where YOUR-USERNAME-HERE is for account setup on [TestPyPI](https://test.pypi.org/project/)

4. Run the tests:

TODO: add instructions

________________________________________________________________________________
## SECTION 4. Tag the release

1. From the project folder:
```bash
git tag -a x.x.x -m "version x.x.x"
git push origin x.x.x
```

* x.x.x is the release number

________________________________________________________________________________
## SECTION 5. Promote to PYPI

1. From the project folder
```bash
python3 -m pip install --upgrade twine
```

2. Upload to pypy:
```bash
python3 -m twine upload dist/*
```

#### End of # py-fortress DEVELOPERS GUIDE