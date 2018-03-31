# py-fortress Command Line Interpreter (CLI) README AUTHENTICATION and AUTHOTIZATION
 
For RBAC0 system management testing.
_____________________________________________________________________________
## Table of Contents
 * SECTION 1. Introduction 
 * SECTION 2. Prerequisites
 * SECTION 3. Run it
___________________________________________________________________________________
## SECTION 1. Introduction

Describe commands contained within CLI program cli-test-auth.py which test drive the [access_mgr](impl/access_mgr.py) APIs.
______________________________________________________________________________
## SECTION 2. Prerequisites

 * Have a working py-fortress env setup by following instructions here: [README](./README.md)
 * Understanding of argument passing rules described here: [README-CLI](./README-CLI.md)
 
___________________________________________________________________________________
## SECTION 3. Run it

1. Prepare your terminal for execution of python3.  From the main dir of the git repo:
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
   * get : maps to access_mgr.session_perms
   * show : displays contents of session to stdout
   * add : maps to access_mgr.add_active_role
   * del : maps to access_mgr.drop_active_role
   
   

### The args are '--' + names contained within these py-fortress entities:
   * [user](model/user.py) - e.g. --uid, --password
   * [perm](model/perm.py) - e.g. --obj_name, --op_name
    
### A Few Tips

   * These commands have a one-to-one mapping to the access APIs.  For example, the auth command maps to the access_mgr.create_session function and check calls access_mgr.check_access.
   * The description of the commands, including required arguments, can be inferred via the api doc inline to the access_mgr module.
   * The session is 'pickled' (serialized) and stored on the file system in executable folder.
   * Call the auth operation first, subsequent ops will use and refresh the session.
   * Constraints on user and roles are enforced.  For example, if user has timeout constraint of 30 (minutes), and the delay between ops for existing session exceeds, it will be deactivated.
   
3. [AdminMgr](impl/admin_mgr.py) Setup test data:

   a. **user add**
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
   b. **role add** - account-mgr
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
   c. **role add** - auditor
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
   d. **user assign** - account-mgr
    ```
    (env)~py-fortress/test$ python3 cli.py user assign --uid 'chorowitz' --role 'account-mgr'
    uid=chorowitz
    role name=account-mgr
    user assign
    success
    ```
   e. **user assign** - auditor
    ```
    (env)~py-fortress/test$ python3 cli.py user assign --uid 'chorowitz' --role 'auditor'
    uid=chorowitz
    role name=auditor
    user assign
    success
    ```
   f. **object add** - page456
    ```
    (env)~py-fortress/test$ python3 cli.py object add --obj_name page456
    obj_name=page456
    object add
    success
    ```
   g. **perm add** - page456.read
    ```
    (env)~py-fortress/test$ python3 cli.py perm add --obj_name page456 --op_name read
    obj_name=page456
    op_name=read
    perm add
    success
    ```
   h. **perm add** - page456.edit
    ```
    (env)~py-fortress/test$ python3 cli.py perm add --obj_name page456 --op_name edit
    obj_name=page456
    op_name=edit
    perm add
    success
    ```
   i. **perm add** - page456.remove
    ```
    (env)~py-fortress/test$ python3 cli.py perm add --obj_name page456 --op_name remove
    obj_name=page456
    op_name=remove
    perm add
    success
    ```
   j. **perm grant** - page456.edit, account-mgr
    ```
    (env)~py-fortress/test$ python3 cli.py perm grant --obj_name page456 --op_name edit --role account-mgr
    obj_name=page456
    op_name=edit
    role name=account-mgr
    perm grant
    success
    ```
   k. **perm grant** - page456.remove, account-mgr
    ```
    (env)~py-fortress/test$ python3 cli.py perm grant --obj_name page456 --op_name remove --role account-mgr
    obj_name=page456
    op_name=remove
    role name=account-mgr
    perm grant
    success
    ```
   l. **perm grant** - page456.edit, auditor 
    ```
    (env)~py-fortress/test$ python3 cli.py perm grant --obj_name page456 --op_name read --role auditor
    obj_name=page456
    op_name=read
    role name=auditor
    perm grant
    success
    ```


3. [AccessMgr](impl/access_mgr.py) Examples:

   a. **auth** - access_mgr.create_session - authenticate, activate roles:
    ```
    (env)~py-fortress/test$ python3 cli_test_auth.py auth --uid 'chorowitz' --password 'secret'
    uid=chorowitz
    auth
    success
    ```
   b. **show** - output user session contents to stdout:
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
   __Display the contents of session.__
   
   c. **check** - access_mgr.check_access - pemission page456.read:
    ```
    (env) smckinn@ubuntu:~/GIT/pyDev/py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name read
    op_name=read
    obj_name=page456
    check
    success
    ```
   __The user has auditor activated so unless timeout validation failed this will succeed.__
   
  d. **check** - access_mgr.check_access - pemission page456.edit:
    ```
    (env) smckinn@ubuntu:~/GIT/pyDev/py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name edit
    op_name=edit
    obj_name=page456
    check
    success
    ```
   __The user has account-mgr activated so unless timeout validation failed this will succeed.__
   
  e. **check** - access_mgr.check_access - pemission page456.remove:
    ```
    (env) smckinn@ubuntu:~/GIT/pyDev/py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name remove
    op_name=remove
    obj_name=page456
    check
    success
    ```
   __The user has account-mgr activated so unless timeout validation failed this will succeed.__
   
   f. **get** - access_mgr.session_perms:
    ```
    (env) smckinn@ubuntu:~/GIT/pyDev/py-fortress/test$ python3 cli_test_auth.py get
    get
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
   __Display all perms allowed for activated roles.__
    
   g. **del** - access_mgr.drop_active_role - auditor:
    ```
    (env) smckinn@ubuntu:~/GIT/pyDev/py-fortress/test$ python3 cli_test_auth.py del --role auditor
    del
    success
    ```
   __RBAC distinguishes between assigned and activated roles.__
        
   h. **check** - access_mgr.check_access - pemission page456.read:
    ```
    (env) smckinn@ubuntu:~/GIT/pyDev/py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name read
    op_name=read
    obj_name=page456
    check
    failed
    ```
   __The auditor role deactivated so even though it's assigned user cannot perform as auditor.__
            
   i. **add** - access_mgr.add_active_role - auditor:
    ```
    (env) smckinn@ubuntu:~/GIT/pyDev/py-fortress/test$ python3 cli_test_auth.py add --role auditor
    op_name=read
    obj_name=page456
    check
    success
    ```
   __Now the user should be allowed to resume audit activities._
                
   j. **check** - access_mgr.check_access - pemission page456.read:
    ```
    (env) smckinn@ubuntu:~/GIT/pyDev/py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name read
    op_name=read
    obj_name=page456
    check
    success
    ```
   __The auditor role activated once again so user can do auditor things again.__
                    
   k. Wait 5 minutes before repeating this command:    
   l. **check** - access_mgr.check_access - pemission page456.read:
    ```
    (env) smckinn@ubuntu:~/GIT/pyDev/py-fortress/test$ python3 cli_test_auth.py check --obj_name page456  --op_name read
    op_name=read
    obj_name=page456
    check
    success
    ```
   __Because the auditor role has timeout constraint set to 5 (minutes), role has been deactivated automatically from the session.__                
    
    
### END OF README