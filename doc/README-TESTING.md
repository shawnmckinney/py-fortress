# py-fortress QUICKSTART
-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Prerequisites
 * SECTION 2. Setup Test Env
 * SECTION 3. Run Integration Tests
 * SECTION 4. Run Simple Test Samples
 * SECTION 5. View the Test Data using Command Line Interpreter (CLI)   
___________________________________________________________________________________
## Document Overview

Instructions to test py-fortress from source.
___________________________________________________________________________________
## SECTION 1. Prerequisites

* Completion of [README-BUILDING](README-BUILDING.md)
* LDAP server configured for Apache Fortress using [README-LDAP-DOCKER](./README-LDAP-DOCKER.md)
________________________________________________________________________________
## SECTION 2. Setup Test Env

1. Prepare the config:

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

2. Now edit config file:
 ```
vi $PATH/py-fortress-cfg.json
```

3. Set the LDAP URI
```
...
"ldap": {
...
"uri": "ldap://localhost",
...
```
*use value obtained during LDAP setup*
        
4. Update the connection parameters (pick one):

    a. apacheds:
    ```
    "dn": "uid=admin,ou=system",
    ```
    
    b. openldap:
    ```
    "dn": "dc=example,dc=com",
    ```

5. Set the structure in DIT:
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
    
6. Save and exit

7. Goto test folder:
 ```
cd rbac/tests
```

8. Prepare your terminal for execution of python3.  From the main dir of the git repo:
```bash
python3 -m venv env
. env/bin/activate
export PYTHONPATH=$(pwd)
pip install "python-ldap>=3.4.0"
pip install "six>=1.16.0"
pip install "ldappool>=3.0.0"
```

9. Run the bootstrap pgm that creates the LDAP node structure, i.e. the *DIT*
```bash
python3 test_dit_dao.py
```
* Locations for these nodes are set in the config file.*
    
__________________________________________________________________________________
## SECTION 3. Integration Tests

These steps are optional and verify the env is working correctly.

1. Run the admin mgr tests:
```
python3 test_admin.py 
```

2. Run the access mgr tests:
```
python3 test_access.py 
```
 
3. Run the review mgr tests:
```
python3 test_review.py 
```
__________________________________________________________________________________
## SECTION 4. Simple Test Samples

Another optional test.  
 
1. Run the samples:
```
python3 test_samples.py 
```

2. View the [test_samples](../rbac/tests/test_samples.py) and learn how RBAC APIs work.

__________________________________________________________________________________
## SECTION 5. View the Test Data using Command Line Interpreter (CLI)

View the test data inserted earlier.

1. Navigate to cli folder:
```bash
cd rbac/cli
```
 
3. user search 
```
$ python3 cli.py user search --uid p
```
    
2. role search 
```
$ python3 cli.py role search --name p
```
    
3. perm search
```
$ python3 cli.py perm search --obj_name p
```

4. More CLI commands
  * [README-CLI](./README-CLI.md) and [README-CLI-AUTH](./README-CLI-AUTH.md) for more operations to test.


#### End of README-TESTING
