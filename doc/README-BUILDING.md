# py-fortress README-BUILDING
-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Prerequisites
 * SECTION 2. Setup Python Runtime and Configure py-fortress Usage
 * SECTION 3. Integration Test
 * SECTION 4. Simple Test Samples 
 * SECTION 5. View the Test Data using Command Line Interpreter (CLI)
___________________________________________________________________________________
## Document Overview

 * Contains instructions to build and test py-fortress
___________________________________________________________________________________
## SECTION 1. Prerequisites

Minimum hardware requirements:
 * 1 Core
 * 1 GB RAM

Minimum software requirements:
 * Linux machine
 * git
 * completion of [README-LDAP-DOCKER](./README-LDAP-DOCKER)
 * Python3 and virtualenv (venv) or system install of the ldap3 python module
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
pyvenv env
. env/bin/activate
python3 -m pip install --upgrade build
python3 -m build
```
4. Install

```bash
pip install py-fortress
```

5. Prepare the config:

Copy sample cfg file:

```bash
cp py-fortress-cfg.json.sample py-fortress-cfg.json
```

sample cfg file is here: [py-fortress-cfg.json.sample](../py-fortress-cfg.json.sample)

6. Now edit config file:
 ```
vi py-fortress-cfg.json
```

7. Set the LDAP URI
```
...
"ldap": {
...
"uri": "ldap://localhost",
...
```
*use value obtained during LDAP setup*
        
8. Update the connection parameters (pick one):

    a. apacheds:
    ```
    "dn": "uid=admin,ou=system",
    ```
    
    b. openldap:
    ```
    "dn": "dc=example,dc=com",
    ```

9. Set the structure in DIT:
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
    
10. Save and exit

11. Run the tests:
 ```
pyvenv env
. env/bin/activate
pip install python-ldap
pip install six
pip install ldappool
export PYTHONPATH=$(pwd)
cd test
```
    
12. Run the bootstrap pgm that creates the LDAP node structure, i.e. the *DIT*
     ```
     python3 test_dit_dao.py 
     ```
    
     *Locations for these nodes are set in the config file.* 
    
__________________________________________________________________________________
## SECTION 3. Integration Tests

These steps are optional and verify the env is working correctly.

1. Run the admin mgr tests:
    ```
    python3 test_admin_mgr.py 
    ```

2. Run the access mgr tests:
    ```
    python3 test_access_mgr.py 
    ```
 
3. Run the review mgr tests:
    ```
    python3 test_review_mgr.py 
    ```
__________________________________________________________________________________
## SECTION 4. Simple Test Samples

Another optional test.  
 
1. Run the samples:
    ```
    python3 test_samples.py 
    ```

2. View the [test_samples](test/test_samples.py) and learn how RBAC APIs work.

__________________________________________________________________________________
## SECTION 5. View the Test Data using Command Line Interpreter (CLI)

View the test data inserted earlier.  
 
1. user search 
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


#### End of README-BUILDING


#### Testing the scripts from source:

Run the tests:
 ```
pyvenv env
. env/bin/activate
pip install python-ldap
pip install six
pip install ldappool
export PYTHONPATH=$(pwd)
cd test
python3 test_admin_mgr.py
python3 test_access_mgr.py
...
```
    
