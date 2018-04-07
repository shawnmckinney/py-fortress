# py-fortress QUICKSTART
-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Prerequisites
 * SECTION 2. Setup Python Runtime and Configure py-fortress Usage
 * SECTION 3. Integration Test
 * SECTION 4. Simple Test Samples 
___________________________________________________________________________________
## Document Overview

 * Contains instructions to install and test py-fortress by source
___________________________________________________________________________________
## SECTION 1. Prerequisites

Minimum hardware requirements:
 * 1 Core
 * 1 GB RAM

Minimum software requirements:
 * Linux machine
 * git
 * Python3 and virtualenv (venv) or system install of the ldap3 python module
 * completion of [README-LDAP-DOCKER](./README-LDAP-DOCKER)
 * completion of [README-INSTALL](./README-INSTALL)  
________________________________________________________________________________
## SECTION 2. Setup py-fortress Runtime

1. Make a test folder:
    ```
    md test    
    cd test
    ```

2. Prepare your terminal for execution of python3.  From the main dir of the git repo:
    ```
    pyvenv env
    . env/bin/activate
    export PYTHONPATH=$(pwd)
    ```
    
3. Install py-fortress
    ```
    pip install py-fortress
    ```

4. Download and edit [py-fortress-cfg.json](https://github.com/shawnmckinney/py-fortress/blob/master/pyfortress/test/py-fortress-cfg.json) config file to test folder:
    ```
    wget https://raw.githubusercontent.com/shawnmckinney/py-fortress/master/pyfortress/test/py-fortress-cfg.json
    vi py-fortress-cfg.json
    ```

5. Set the LDAP Port
    ```
    ...
    "ldap": {
      ...
      "port": 32768,
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
    "dn": "cn=Manager,dc=example,dc=com",
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
    
8. Save and exit config file.

9. Run the bootstrap pgm that creates the LDAP node structure, i.e. the *DIT*
    ```
    initldap 
    ```
    *initldap is a python script, created during install of py-fortress package, that maps here: pyfortress.test.test_dit_dao*
    *Locations for these nodes are set in the config file.* 
    __________________________________________________________________________________
## SECTION 3. Integration Tests

These steps are optional and verify the env is working correctly.

1. Run the admin mgr tests:
    ```
    $ python3 -m pyfortress.test.test_admin_mgr 
    ```

2. Run the access mgr tests:
    ```
    $ python3 -m pyfortress.test.test_access_mgr
    ```
 
3. Run the review mgr tests:
    ```
    $ python3 -m pyfortress.test.test_review_mgr 
    ```
__________________________________________________________________________________
## SECTION 4. Simple Test Samples

Another optional test.  
 
1. Run the samples:
    ```
    $ python3 -m pyfortress.test.test_samples 
    ```

2. View the [test_samples](../test/test_samples.py) and learn how RBAC APIs work.

# END README-QUICKSTART