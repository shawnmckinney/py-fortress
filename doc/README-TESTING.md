# py-fortress QUICKSTART
-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Prerequisites
 * SECTION 2. Setup Test Env
 * SECTION 3. Integration Tests
 * SECTION 4. Simple Test Samples
 * SECTION 5. View the Test Data using Command Line Interpreter (CLI)   
___________________________________________________________________________________
## Document Overview

Instructions to test py-fortress from source.
___________________________________________________________________________________
## SECTION 1. Prerequisites

Minimum hardware requirements:
 * 1 Core
 * 1 GB RAM
 
Minimum software requirements:
 * python-ldap dependencies installed [README-UPGRADE-PYTHON](./README-UPGRADE-PYTHON.md)
 * LDAP server configured for Apache Fortress using [README-LDAP-DOCKER](./README-LDAP-DOCKER.md)
________________________________________________________________________________
## SECTION 2. Setup Test Env

1. Clone py-fortress
```
git clone https://github.com/shawnmckinney/py-fortress.git
```

2. Change directory into root folder of project:
```
cd py-fortress
```

3. Prepare the config:

From the project root folder, copy sample cfg file:

```bash
cp py-fortress-cfg.json.sample $PATH/py-fortress-cfg.json
```

Where PATH equals one of the following:
a. current directory
b. user home directory
c. /etc/pyfortress
d. pointed to by: ```export PYFORTRESS_CONF=...```

sample cfg file is here: [py-fortress-cfg.json.sample](../py-fortress-cfg.json.sample)

4. Now edit config file:
 ```
vi $PATH/py-fortress-cfg.json
```

5. Set the LDAP URI
```
...
"ldap": {
...
"uri": "ldap://localhost:389",
...
```
*use value obtained during LDAP setup*
        
6. Update the connection parameters (pick one):

    a. apacheds:
    ```
    "dn": "uid=admin,ou=system",
    ```
    
    b. openldap:
    ```
    "dn": "dc=example,dc=com",
    ```

7. Set the structure in DIT:
    ```
    ...
    "dit": {
        "suffix": "dc=example,dc=com",
        "users": "People",
        "roles": "Roles",
        "perms": "Perms"
    },
    ...    
    ```
    *if in doubt use the defaults*
    
8. Save and exit

9. Prepare your terminal for execution of python3.  From the main dir of the git repo:
```bash
python3 -m venv env
. env/bin/activate
export PYTHONPATH=$(pwd)
pip install "python-ldap>=3.4.2"
pip install "six>=1.16.0"
pip install "ldappool>=3.0.0"
```

10. Run the bootstrap pgm that creates the LDAP node structure, i.e. the *DIT*
```bash
python3 rbac/tests/test_dit_dao.py
```
* Locations for these nodes are set in the config file.*
    
__________________________________________________________________________________
## SECTION 3. Integration Tests

These steps are optional and verify the env is working correctly.

1. Run the admin mgr tests:
```bash
python3 rbac/tests/test_admin.py 
```

2. Run the access mgr tests:
```bash
python3 rbac/tests/test_access.py 
```
 
3. Run the review mgr tests:
```bash
python3 rbac/tests/test_review.py 
```
__________________________________________________________________________________
## SECTION 4. Simple Test Samples

Another optional test.  
 
1. Run the samples:
```bash
python3 rbac/tests/test_samples.py 
```

2. View the [test_samples](../rbac/tests/test_samples.py) and learn how RBAC APIs work.

__________________________________________________________________________________
## SECTION 5. View the Test Data using Command Line Interpreter (CLI)

View the test data inserted earlier.

1. user search 
```bash
$ python3 rbac/cli/cli.py user search --uid p
```
    
2. role search 
```bash
$ python3 rbac/cli/cli.py role search --name p
```
    
3. perm search
```bash
$ python3 rbac/cli/cli.py perm search --obj_name p
```

4. More CLI commands
  * [README-CLI](./README-CLI.md) and [README-CLI-AUTH](./README-CLI-AUTH.md) for more operations to test.


#### End of README-TESTING
