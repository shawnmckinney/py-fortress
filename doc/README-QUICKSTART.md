# py-fortress QUICKSTART
-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Prerequisites
 * SECTION 2. Setup Test Env
 * SECTION 3. Using Command Line Interpreter (CLI)
___________________________________________________________________________________
## Document Overview

Instructions to install py-fortress and do some basic testing.
___________________________________________________________________________________
## SECTION 1. Prerequisites

Minimum hardware requirements:
 * 1 Core
 * 1 GB RAM

Prerequisites:
 * LDAP server configured for Apache Fortress using [README-LDAP-DOCKER](./README-LDAP-DOCKER.md)
 * python-ldap dependencies installed [README-UPGRADE-PYTHON](./README-UPGRADE-PYTHON.md)
________________________________________________________________________________
## SECTION 2. Setup Test Env

Follow these steps to install py-fortress package and get it pointing to your LDAP server.

1. Make a test folder:
```
mkdir test    
cd test
```

2. Prepare your terminal for execution of python3.  From the main dir of the git repo:
```
python3 -m venv env
. env/bin/activate
export PYTHONPATH=$(pwd)
```
    
3. Install py-fortress
```
pip install py-fortress
```

4. Download and edit [py-fortress-cfg.json](https://github.com/shawnmckinney/py-fortress/blob/master/test/py-fortress-cfg.json) config file to test folder:
 ```
cp ./env/conf/py-fortress-cfg.json.sample py-fortress-cfg.json
vi py-fortress-cfg.json
```

Where PATH equals one of the following:
a. current directory
b. user home directory
c. /etc/pyfortress
d. pointed to by: ```export PYFORTRESS_CONF=...```

2. Set the LDAP Port
```
...
"ldap": {
      ...
      "uri": "ldap://localhost",
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
    
8. Save and exit config file.

9. Run the bootstrap pgm that creates the LDAP node structure, i.e. the *DIT*
```
initldap 
```
*initldap is a python script, created during install of py-fortress package, that maps here: pyfortress.tests.test_dit_dao*
*Locations for these nodes are set in the config file.* 
________________________________________________________________________________________
## SECTION 3. Using Command Line Interpreter (CLI)

View the test data.  
 
1. user search 
    ```
    $ cli user search --uid p
    ```
    
2. role search 
    ```
    $ cli role search --name p
    ```
    
3. perm search
    ```
    $ cli perm search --obj_name p
    ```

4. More CLI commands
  * [README-CLI](./README-CLI.md) and [README-CLI-AUTH](./README-CLI-AUTH.md) for more operations to test.


#### End of README-QUICKSTART