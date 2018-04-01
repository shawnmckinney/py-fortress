# Guide to Command Line Interpreter (CLI) for RBAC0 SYSTEM Testing
 
Instructions to load a simple RBAC policy and use the cli-test-auth.py program that drives py-fortress [access_mgr](impl/access_mgr.py) APIs.
______________________________________________________________________________
## Prerequisites

 * Have a working py-fortress env setup by following instructions here: [README](./README.md)
 * Understanding of argument passing rules described here: [README-CLI](./README-CLI.md)
 
## Sample RBAC0 Policy

This tutorial covers the basics, RBAC Core:  Many-to-many relationships between users, roles and perms and selective role activations.
py-fortress adds to the mix one non-standard feature: constraint validations on user and role entity activation. 
 
The simple policy includes constraints later we'll demo a role timing out of the session.

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
    cd test
    ```
    
2. To run the CLI:
    ```
    python3 cli-test-auth.py operation --arg1 --arg2 ...  
    ```
    
### The operation maps to (pick one):
[AccessMgr](impl/access_mgr.py)
   * auth : maps to access_mgr.create_session
   * check : maps to access_mgr.check_access
   * roles : maps to access_mgr.session_roles   
   * perms : maps to access_mgr.session_perms
   * show : displays contents of session to stdout
   * add : maps to access_mgr.add_active_role
   * del : maps to access_mgr.drop_active_role

### The args are '--' + names contained within these py-fortress entities:
   * [user](model/user.py) - e.g. --uid, --password
   * [perm](model/perm.py) - e.g. --obj_name, --op_name
    
### Command Usage Tips
   * The description of the commands, i.e. required and optional arguments, can be inferred via the api doc inline to the access_mgr module.
   * This program 'pickles' (serializes) the RBAC session to a file called sess.pickle, and places in the executable folder.  This simulates an RBAC runtime to test these commands.
   * Call the auth operation first, subsequent ops will use and refresh the session.
   * Constraints on user and roles are enforced. For example, if user has timeout constraint of 30 (minutes), and the delay between ops for existing session exceeds, it will be deactivated.
_______________________________________________________________________________   
## Setup Test Data With ([AdminMgr](impl/admin_mgr.py)) CLI

This section requires another utility, [README-CLI.md](./README-CLI.md), to insert the RBAC policy that will be tested in the section following.

From the Python3 runtime terminal, enter the following commands, from the test folder:  

1. **user add** - chorowitz
   
    ```
    (env)~py-fortress/test$ python3 cli.py user add --uid chorowitz --password 'secret' --timeout 30 --begin_date 20180101 --end_date none --day_mask 1234567 --description 'for testing only'
    uid=chorowitz
    description=for testing only
    end_date=none
    begin_date=20180101
    day_mask=1234567
    timeout=30
    name=chorowitz
    user add
    success
    ```
    
2. **role add** - account-mgr
   
    ```
    (env)~py-fortress/test$ python3 cli.py role add --name 'account-mgr' --timeout 30 --begin_date 20180101 --end_date none --day_mask 1234567
    name=account-mgr
    end_date=none
    begin_date=20180101
    day_mask=1234567
    timeout=5
    role add
    success
    ```
    
3. **role add** - auditor
   
    ```
    (env)~py-fortress/test$ python3 cli.py role add --name 'auditor' --timeout 5 --begin_date 20180101 --end_date none --day_mask 1234567
    name=auditor
    end_date=none
    begin_date=20180101
    day_mask=1234567
    timeout=5
    role add
    success
    ```
    
4. **user assign** - chorowitz to role account-mgr
   
    ```
    (env)~py-fortress/test$ python3 cli.py user assign --uid 'chorowitz' --role 'account-mgr'
    uid=chorowitz
    role name=account-mgr
    user assign
    success
    ```
    
5. **user assign** - chorowitz to role auditor
   
    ```
    (env)~py-fortress/test$ python3 cli.py user assign --uid 'chorowitz' --role 'auditor'
    uid=chorowitz
    role name=auditor
    user assign
    success
    ```
    
6. **object add** - page456
   
    ```
    (env)~py-fortress/test$ python3 cli.py object add --obj_name page456
    obj_name=page456
    object add
    success
    ```
    
7. **perm add** - page456.read
   
    ```
    (env)~py-fortress/test$ python3 cli.py perm add --obj_name page456 --op_name read
    obj_name=page456
    op_name=read
    perm add
    success
    ```
    
8. **perm add** - page456.edit
   
    ```
    (env)~py-fortress/test$ python3 cli.py perm add --obj_name page456 --op_name edit
    obj_name=page456
    op_name=edit
    perm add
    success
    ```
    
9. **perm add** - page456.remove
   
    ```
    (env)~py-fortress/test$ python3 cli.py perm add --obj_name page456 --op_name remove
    obj_name=page456
    op_name=remove
    perm add
    success
    ```
    
10. **perm grant** - page456.edit to role account-mgr
   
    ```
    (env)~py-fortress/test$ python3 cli.py perm grant --obj_name page456 --op_name edit --role account-mgr
    obj_name=page456
    op_name=edit
    role name=account-mgr
    perm grant
    success
    ```
    
11. **perm grant** - page456.remove to role account-mgr
   
    ```
    (env)~py-fortress/test$ python3 cli.py perm grant --obj_name page456 --op_name remove --role account-mgr
    obj_name=page456
    op_name=remove
    role name=account-mgr
    perm grant
    success
    ```
    
12. **perm grant** - page456.read to role auditor 
   
    ```
    (env)~py-fortress/test$ python3 cli.py perm grant --obj_name page456 --op_name read --role auditor
    obj_name=page456
    op_name=read
    role name=auditor
    perm grant
    success
    ```
________________________________________________________________________________
## Perform [AccessMgr](impl/access_mgr.py) Commands

From the Python3 runtime, enter the following commands:

1. **auth** - access_mgr.create_session - authenticate, activate roles:
   
    ```
    (env)~py-fortress/test$ python3 cli_test_auth.py auth --uid 'chorowitz' --password 'secret'
    uid=chorowitz
    auth
    success
    ```
   _The session has been created and stored to a file in the current directory, called sess.pickle, and used by commands that follow._
    
2. **show** - output user session contents to stdout:
   
    ```
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli_test_auth.py show
    show
    session
        warnings: None
        session_id: None
        error_id: None
        expiration_seconds: None
        user: <model.user.User object at 0x7fdfb2745208>
        grace_logins: None
        message: None
        timeout: None
        is_authenticated: True
        last_access: <util.current_date_time.CurrentDateTime object at 0x7fdfb2743e10>
    user
        department_number: 
        l: 
        role_constraints: [<model.constraint.Constraint object at 0x7fdfb2745320>, <model.constraint.Constraint object at 0x7fdfb2745470>]
        postal_code: 
        title: 
        constraint: <model.constraint.Constraint object at 0x7fdfb2745550>
        reset: []
        phones: 
        locked_time: []
        emails: 
        cn: chorowitz
        ou: 
        physical_delivery_office_name: 
        roles: ['account-mgr', 'auditor']
        pw_policy: 
        room_number: 
        mobiles: 
        description: for testing only
        uid: chorowitz
        system: []
        internal_id: 4a7a68ae-d0c3-4328-98dc-e7f64739ed67
        employee_type: 
        sn: chorowitz
        props: 
        dn: uid=chorowitz,ou=People,dc=example,dc=com
        display_name: 
     User Constraint:
            raw: 
     User-Role Constraint[1]:
            day_mask: 1234567
            begin_time: 
            name: account-mgr
            end_lock_date: 
            begin_lock_date: 
            begin_date: 20180101
            end_time: 
            timeout: 30
            raw: account-mgr$30$$$20180101$none$$$1234567
            end_date: none
     User-Role Constraint[2]:
            day_mask: 1234567
            begin_time: 
            name: auditor
            end_lock_date: 
            begin_lock_date: 
            begin_date: 20180101
            end_time: 
            timeout: 5
            raw: auditor$5$$$20180101$none$$$1234567
            end_date: none
    *************** user *******************    
    success
    ```
   _Display the contents of session including user atributes, status, role activations._
   
3. **check** - access_mgr.check_access - perm page456.read:
   
    ```
    (env)~py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name read
    op_name=read
    obj_name=page456
    check
    success
    ```
   _The user has auditor activated so unless timeout validation failed this will succeed._
   
4. **check** - access_mgr.check_access - perm page456.edit:
   
    ```
    (env)~py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name edit
    op_name=edit
    obj_name=page456
    check
    success
    ```
   _The user has account-mgr activated so unless timeout validation failed this will succeed._
   
5. **check** - access_mgr.check_access - perm page456.remove:
   
    ```
    (env)~py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name remove
    op_name=remove
    obj_name=page456
    check
    success
    ```
   _The user has account-mgr activated so unless timeout validation failed this will succeed._
   
6. **perms** - access_mgr.session_perms:
   
    ```
    (env)~py-fortress/test$ python3 cli_test_auth.py get
    perms
    page456.read:0
        description: 
        abstract_name: page456.read
        obj_id: 
        props: 
        type: 
        roles: ['auditor']
        users: 
        dn: ftOpNm=read,ftObjNm=page456,ou=Perms,dc=example,dc=com
        internal_id: d6887434-050c-48d8-85b0-7c803c9fcf07
        obj_name: page456
        op_name: read
    page456.edit:1
        description: 
        abstract_name: page456.edit
        obj_id: 
        props: 
        type: 
        roles: ['account-mgr']
        users: 
        dn: ftOpNm=edit,ftObjNm=page456,ou=Perms,dc=example,dc=com
        internal_id: 02189535-4b39-4058-8daf-af0e09b0d235
        obj_name: page456
        op_name: edit
    page456.remove:2
        description: 
        abstract_name: page456.remove
        obj_id: 
        props: 
        type: 
        roles: ['account-mgr']
        users: 
        dn: ftOpNm=remove,ftObjNm=page456,ou=Perms,dc=example,dc=com
        internal_id: 10dea5d1-ff1d-4c3d-90c8-edeb4c7bb05b
        obj_name: page456
        op_name: remove
    success
    ```
   _Display all perms allowed for activated roles._
    
7. **del** - access_mgr.drop_active_role - deactivate auditor role:
   
    ```
    (env)~py-fortress/test$ cli_test_auth.py del --role auditor
    del
    success
    ```
   _RBAC distinguishes between assigned and activated roles_
        
8. **roles** - access_mgr.session_roles:
   
    ```
    (env)~py-fortress/test$ python3 cli_test_auth.py roles
    roles
    account-mgr:0
        begin_time: 
        raw: account-mgr$30$$$20180101$none$$$1234567
        begin_lock_date: 
        end_date: none
        name: account-mgr
        end_time: 
        timeout: 30
        day_mask: 1234567
        begin_date: 20180101
        end_lock_date: 
    success    
    ```
   _Notice the auditor role is not displayed because it is no longer active in session._
        
9. **check** - access_mgr.check_access - perm page456.read:
   
    ```
    (env)~py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name read
    op_name=read
    obj_name=page456
    check
    failed
    ```
   _Although the auditor role is still assigned to the user, it's deactivated from the session so user cannot perform as one._
            
10. **add** - access_mgr.add_active_role - auditor:
   
    ```
    (env)~py-fortress/test$ python3 cli_test_auth.py add --role auditor
    op_name=read
    obj_name=page456
    check
    success
    ```
    
    _Now the user resumes auditor activities._
                
11. **roles** - access_mgr.session_roles:
   
    ```
    (env)~py-fortress/test$ python3 cli_test_auth.py roles
    roles
    account-mgr:0
        begin_time: 
        raw: account-mgr$30$$$20180101$none$$$1234567
        begin_lock_date: 
        end_date: none
        name: account-mgr
        end_time: 
        timeout: 30
        day_mask: 1234567
        begin_date: 20180101
        end_lock_date: 
    auditor:1
        end_date: none
        day_mask: 1234567
        raw: auditor$5$$$20180101$none$$$1234567
        begin_date: 20180101
        end_lock_date: 
        timeout: 5
        begin_time: 
        name: auditor
        end_time: 
        begin_lock_date:     success
    success            
    ```
    _Notice the audit role has been reactivated into the session._
        
12. **check** - access_mgr.check_access - perm page456.read:
   
    ```
    (env)~py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name read
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
    (env)~py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name read
    op_name=read
    obj_name=page456
    check
    failed
    ```
    
    _Because the auditor role has timeout constraint set to 5 (minutes), role has been deactivated automatically from the session._              
    
    
### END OF README