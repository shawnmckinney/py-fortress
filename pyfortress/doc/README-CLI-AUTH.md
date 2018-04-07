# Guide to Command Line Interpreter (CLI) for RBAC0 SYSTEM Testing
 
Instructions to load a simple RBAC policy and use the cli-test-auth.py program that drives py-fortress [access_mgr](../impl/access_mgr.py) APIs.
______________________________________________________________________________
## Prerequisites

Completed [README-QUICKSTART](.README-QUICKSTART.md)
______________________________________________________________________________
## Sample RBAC0 Policy

This tutorial covers the basics, RBAC Core:  Many-to-many relationships between users, roles and perms and selective role activations.
py-fortress adds to the mix one non-standard feature: constraint validations on user and role entity activation. 
 
The simple policy includes constraints being setup on user and role.  Later we'll demo a role timing out of the session.

### Users

| uid           | timeout | begin_time | end_time | ...   |
| ------------- | ------- | ---------- | -------- | ----- |
| chorowitz     | 30min   |            |          |       |

### Roles

| name          | timeout | begin_time | end_time | ...   |
| ------------- | ------- | ---------- | -------- | ----- |
| account-mgr   | 30min   |            |          |       |
| auditor       |  5min   |            |          |       |

 _constraints are optional and include time, date, day and lock date validations_

### User-to-Role Assignments

| user          | account-mgr   | auditor       |
| ------------- | ------------- | ------------- |
| chorowitz     | true          | true          |

### Permissions

| obj_name      | op_name        |
| ------------- | -------------- |
| page456       | edit           |
| page456       | remove         |
| page456       | read           |

### Role-to-Permissions

| role          | page456.edit   | page456.remove | page456.read   |
| ------------- | -------------- | -------------- | -------------- |
| account-mgr   | true           | true           | false          |
| auditor       | false          | false          | true           |
___________________________________________________________________________________
## Run it

Here we'll load the policy defined above.

1. First, prepare a terminal for execution of python3.  From the main dir of the git repo:
    ```
    pyvenv env
    ```
    
2. The syntax for py-fortress system commands:
    ```
    clitest operation --arg1 --arg2 ...  
    ```
    *executes a package script that maps here: pyfortress.test.cli_test_auth*
    
### The operation is (pick one):
   * auth => access_mgr.create_session
   * check => access_mgr.check_access
   * roles => access_mgr.session_roles   
   * perms => access_mgr.session_perms
   * show => displays contents of session to stdout
   * add => access_mgr.add_active_role
   * drop => access_mgr.drop_active_role
   
   _Where operations map to functions here_ [access_mgr.py](impl/access_mgr.py)

### The args are ‘–‘ + attribute name + attribute value
   * --uid, --password from [user.py](../model/user.py)
   * --obj_name, --op_name, --obj_id from [perm.py](../model/perm.py)
   * --role used for the role name
    
### Command Usage Tips
   * The description of the commands, i.e. required and optional arguments, can be inferred via the api doc inline to the access_mgr module.
   * This program 'pickles' (serializes) the RBAC session to a file called sess.pickle, and places in the executable folder.  This simulates an RBAC runtime to test these commands.
   * Call the auth operation first, subsequent ops will use and refresh the session.
   * Constraints on user and roles are enforced. For example, if user has timeout constraint of 30 (minutes), and the delay between ops for existing session exceeds, it will be deactivated.
   * More on argument format: [README-CLI](./README-CLI.md)
_______________________________________________________________________________   
## Setup an RBAC Policy Using ([admin_mgr](../impl/admin_mgr.py)) CLI

* To setup RBAC test data, we'll be using another utility that was introduced here:  [README-CLI](./README-CLI.md).

From the py-fortress/test folder, enter the following commands:  

1. **user add** - chorowitz
   
    ```
    $ cli user add --uid chorowitz --password 'secret' --timeout 30
    ``` 
   _user chorowitz has a 30 minute inactivity timeout_
    
2. **role add** - account-mgr
   
    ```
    $ cli role add --name 'account-mgr'
    ```
    
3. **role add** - auditor
   
    ```
    $ cli role add --name 'auditor' --timeout 5
    ```
   auditor has a 5 minute inactivity timeout, more later about this..._    
    
4. **user assign** - chorowitz to role account-mgr
   
    ```
    $ cli user assign --uid 'chorowitz' --role 'account-mgr'
    ```
    
5. **user assign** - chorowitz to role auditor
   
    ```
    $ cli user assign --uid 'chorowitz' --role 'auditor'
    ```
    
6. **object add** - page456
   
    ```
    $ cli object add --obj_name page456
    ```
    
7. **perm add** - page456.read
   
    ```
    $ cli perm add --obj_name page456 --op_name read
    ```
    
8. **perm add** - page456.edit
   
    ```
    $ cli perm add --obj_name page456 --op_name edit
    ```
    
9. **perm add** - page456.remove
   
    ```
    $ cli perm add --obj_name page456 --op_name remove
    ```
    
10. **perm grant** - page456.edit to role account-mgr
   
    ```
    $ cli perm grant --obj_name page456 --op_name edit --role account-mgr
    ```
    
11. **perm grant** - page456.remove to role account-mgr
   
    ```
    $ cli perm grant --obj_name page456 --op_name remove --role account-mgr
    ```
    
12. **perm grant** - page456.read to role auditor 
   
    ```
    $ python3 cli.py perm grant --obj_name page456 --op_name read --role auditor
    ```
________________________________________________________________________________
## Run the [access_mgr](../impl/access_mgr.py) CLI

From the py-fortress/test folder, enter the following commands:

1. **auth** - access_mgr.create_session - authenticate, activate roles:

    ```
    $ clitest auth --uid 'chorowitz' --password 'secret'
    ```
    Command outputs to stdout the operation name, arguments and the result:   
    ```
    uid=chorowitz
    auth
    success
    ```
   _The session has been created and stored to a file in the current directory, called sess.pickle, and used by commands that follow._   
    
2. **show** - output user session contents to stdout:
   
    ```
    $ clitest show
    show
    session
        is_authenticated: True
        ...
    user
        uid: chorowitz
        internal_id: 552c1a24-5087-4458-98f1-8c60167a8b7c
        ...
    User Constraint:
            name: chorowitz
            timeout: 30
    User-Role Constraint[1]:
            name: account-mgr
    User-Role Constraint[2]:
            name: auditor
            timeout: 5
    success    
    ```
   _Display the contents of session including user atributes, status, role activations._
   
3. **check** - access_mgr.check_access - perm page456.read:
   
    ```
    $ clitest check --obj_name page456  --op_name read
    op_name=read
    obj_name=page456
    check
    success
    ```
   _The user has auditor activated so unless timeout validation failed this will succeed._
   
4. **check** - access_mgr.check_access - perm page456.edit:
   
    ```
    $ clitest check --obj_name page456  --op_name edit
    op_name=edit
    obj_name=page456
    check
    success
    ```
   _The user has account-mgr activated and will succeed._
   
5. **check** - access_mgr.check_access - perm page456.remove:
   
    ```
    $ clitest check --obj_name page456  --op_name remove
    op_name=remove
    obj_name=page456
    check
    success
    ```
   _The user has account-mgr activated and will succeed._
   
6. **perms** - access_mgr.session_perms:
   
    ```
    $ clitest perms
    perms
    page456.read:0
        abstract_name: page456.read
        roles: ['auditor']
        internal_id: d6887434-050c-48d8-85b0-7c803c9fcf07
        obj_name: page456
        op_name: read
    page456.edit:1
        abstract_name: page456.edit
        roles: ['account-mgr']
        internal_id: 02189535-4b39-4058-8daf-af0e09b0d235
        obj_name: page456
        op_name: edit
    page456.remove:2
        abstract_name: page456.remove
        roles: ['account-mgr']
        internal_id: 10dea5d1-ff1d-4c3d-90c8-edeb4c7bb05b
        obj_name: page456
        op_name: remove
    success
    ```
   _Display all perms allowed for activated roles._
    
7. **drop** - access_mgr.drop_active_role - deactivate auditor role:
   
    ```
    $ clitest drop --role auditor
    drop
    role=auditor    
    success
    ```
   _RBAC distinguishes between assigned and activated roles_
        
8. **roles** - access_mgr.session_roles:
   
    ```
    $ clitest roles
    roles
    account-mgr:0
        raw: account-mgr$30$$$20180101$none$$$1234567
        name: account-mgr
        timeout: 30
    success    
    ```
   _Notice the auditor role is not displayed because it is no longer active in session._
        
9. **check** - access_mgr.check_access - perm page456.read:
   
    ```
    $ clitest check --obj_name page456  --op_name read
    op_name=read
    obj_name=page456
    check
    failed
    ```
   _Although the auditor role is still assigned to the user, it's deactivated from the session so user cannot perform as one._
            
10. **add** - access_mgr.add_active_role - auditor:
   
    ```
    $ clitest add --role auditor    
    add
    role=auditor    
    success
    ```
    
    _Now the user resumes auditor activities._
                
11. **roles** - access_mgr.session_roles:
   
    ```
    $ clitest roles
    roles
    account-mgr:0
        raw: account-mgr$30$$$20180101$none$$$1234567
        name: account-mgr
        timeout: 30
    auditor:1
        raw: auditor$5$$$20180101$none$$$1234567
        timeout: 5
        name: auditor
    success            
    ```
    _Notice the audit role has been reactivated into the session._
        
12. **check** - access_mgr.check_access - perm page456.read:
   
    ```
    $ clitest check --obj_name page456  --op_name read
    op_name=read
    obj_name=page456
    check
    success
    ```
    
    _Because the auditor role was reactivated, the user may resume auditor activities._
                       
13. Wait 5 minutes before performing the next step. 

    _Allow enough time for the auditor role timeout to occur before moving to the next step.  Now, if you run the roles command, the auditor role will once again be missing._
                          
14. **check** - access_mgr.check_access - perm page456.read:
   
    ```
    $ clitest check --obj_name page456  --op_name read
    op_name=read
    obj_name=page456
    check
    failed
    ```
    
    _Because the auditor role has timeout constraint set to 5 (minutes), role has been deactivated automatically from the session._              
    
    
#### End of README-CLI-AUTH