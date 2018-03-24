# py-fortress Command Line Interpreter (CLI) README 

-------------------------------------------------------------------------------
## Table of Contents
 * SECTION 1. Introduction 
 * SECTION 2. Prerequisites
 * SECTION 3. Run it
___________________________________________________________________________________
## SECTION 1. Introduction

The py-fortress CLI drives the [admin_mgr](impl/admin_mgr.py) APIs.
______________________________________________________________________________
## SECTION 2. Prerequisites

 * Have a working py-fortress env setup by following instructions here: [README](./README.md)
___________________________________________________________________________________
## SECTION 3. Run it

1. Prepare your terminal for execution of python3.  From the main dir of the git repo:
    ```
    pyvenv env
    cd test
    ```
    
2. Run the CLI mgr tests:
    ```
    python3 cli.py entity operation --[entity attribute set] 
    ```
    
    where entity is (pick one):
    * user
    * role
    * object
    * perm
    
    and the operation is (pick one):
    * add
    * mod
    * del
    * assign
    * deassign
    * grant
    * revoke
    
    The args are '--' + names contained within the py-fortress entities:
    * [user](model/user.py)
    * [role](model/role.py)
    * [object](model/object.py)
    * [perm](model/pern.py)
    
    Tips:
    * These commands follow exact same rules as the [admin_mgr](impl/admin_mgr.py) APIs.  To understand usage, including required arguments, view its inline code doc.
    * The output will echo the arguments and result.
    * user and perm entities require the *--role** arg for *assign*, *deassign*, *grant*, and *revoke* operations
    
3. Examples

    a. user add
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py user add --uid 'chorowitz' --password 'secret' --description 'added with py-fortress cli'
    uid=chorowitz
    description=added with py-fortress cli
    process_user,add
    success
    ````
    b. user mod
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py user mod --uid 'chorowitz' --l 'my location' --ou 'my-ou' --department_number 123
    uid=chorowitz
    department_number=123
    l=my location
    ou=my-ou
    process_user,update
    success
    ````
    c. user del
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py user del --uid 'chorowitz'
    uid=chorowitz
    process_user,delete
    success    
    ````
    d. user assign
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py user assign --uid 'chorowitz' --role 'account-mgr'
    uid=chorowitz
    role name=account-mgr
    process_user,assign
    success
    ````
    e. user deassign
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py user deassign --uid 'chorowitz' --role 'account-mgr'
    uid=chorowitz
    role name=account-mgr
    process_user,deassign
    success    
    ````
    f. role add
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py role add --name 'account-mgr'
    name=account-mgr
    process_role,add
    success
    ````
    g. role mod
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py role mod --name 'account-mgr' --description 'this desc is optional'
    description=cli test role
    name=account-mgr
    process_role,mod
    success    
    ````
    h. role del
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py role del --name 'account-mgr'
    name=account-mgr
    process_role,delete
    success    
    ````
    i. object add
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py object add --obj_name page456
    obj_name=page456
    process_object,add
    success
    ````
    j. object mod
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py object mod --obj_name page456 --description 'optional arg' --ou 'another optional arg'
    obj_name=page456
    ou=another optional arg
    description=optional arg
    process_object,update
    success
    ````
    k. object del
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py object del --obj_name page789
    obj_name=page789
    process_object,delete
    success
    ````
    l. perm add
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py perm add --obj_name page456 --op_name read
    obj_name=page456
    op_name=read
    process_perm,add
    success
    ````
    m. perm mod
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py perm mod --obj_name page456 --op_name read --description 'useful for human readable perm name'
    obj_name=page456
    op_name=read
    description=useful for human readable perm name
    process_perm,update
    success    
    ````
    n. perm del
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py perm del --obj_name page456 --op_name search
    obj_name=page456
    op_name=search
    process_perm,delete
    success
    ````
    o. perm grant
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py perm grant --obj_name page456 --op_name update --role account-mgr
    obj_name=page456
    op_name=update
    role name=account-mgr
    process_perm,grant
    success
    ````
    p. perm revoke
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py perm revoke --obj_name page456 --op_name update --role account-mgr
    obj_name=page456
    op_name=update
    role name=account-mgr
    process_perm,revoke
    success    
    ````
    
### END OF README