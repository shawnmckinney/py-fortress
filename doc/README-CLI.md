# py-fortress Command Line Interpreter (CLI) README 
 
For RBAC0 administration and review..
_____________________________________________________________________________
## Table of Contents
 * SECTION 1. Introduction 
 * SECTION 2. Prerequisites
 * SECTION 3. Run it
___________________________________________________________________________________
## SECTION 1. Introduction

The py-fortress CLI drive the [admin](../impl/admin.py) and [review](../impl/review.py) APIs.
______________________________________________________________________________
## SECTION 2. Prerequisites

* Completed [README-QUICKSTART](.README-QUICKSTART.md)
___________________________________________________________________________________
## SECTION 3. Run it

1. Prepare your terminal for execution of python3.  From the main dir of your test directory:
```
python3 -m venv env
. env/bin/activate
```
    
2. To run the CLI:
```
cli entity operation --arg1 --arg2 ...  
```
   *executes a package script that maps here: pyfortress.test.cli*    
    
### Where entity is (pick one):
   * user
   * role
   * object
   * perm

### The operation is (pick one):
   * add
   * mod
   * del
   * assign
   * deassign
   * grant
   * revoke
   * read
   * search

### The args are '--' + names contained within these py-fortress entities:
   * [user](src/model/user.py)
   * [role](src/model/role.py)
   * [object](src/model/perm_object.py)
   * [perm](src/model/perm.py)
   * [constraint](src/model/constraint.py)

### Argument Format
   * Consists of two dashes ‘- -‘ plus the attribute name and value pair, with a space between them.    
   ````
   --attribute_name value
   ````

   * if an attribute value contains white space,  enclose in single ‘ ‘ or double tics ” “.    
   ```
   --attribute_name 'some value' --attribute_name2 "still more values"
   ```

   For example, a perm grant:
   ```
   $ cli perm grant --obj_name myobj --op_name add --role 'my role'
   $ python3 -m pyfortress.test.cli
   ```

   * This command invokes Python’s runtime with the program name, cli.py, followed by an entity type, operation name and multiple name-value pairs.
   * The above used *–role* is the only argument that isn’t an entity attribute name.  It’s used on user assign, deassign, perm grant, revoke operations.
   
### Arguments as Lists
   * list of string values, separated by whitespace
   
#### The following arguments are lists

   **phones**     
   
    --phones '+33 401 851 4679' '1-212-251-1111' '(028) 9024 6609'
    
   **mobiles**
    
    --mobiles ' 017x-1234567' '+44 020 7234 3456' '1-212-650-9632'
   
   **emails**
    
    --emails  'f.lst@somewhere.com' 'myaccount@gmail.com' 'myworkaccount@company.com'

   **props**
   
    --props  'name1:value1', 'name2:value2', 'name3:value3' 
   _Each value contains a name:value pair._

### Arguments as Constraint

Both the user and role entity support adding temporal [constraint](src/model/constraint.py)
   
#### The following arguments comprise constraint:

   **name** : label for user, i.e uid
    
    --name foo3   
   _For user, this can be any safe text.  For role, it must already be passed in, with the role's name._
   
   **timeout** : 99 - set the integer timeout that contains max time (in minutes) that entity may remain inactive.
    
    --timeout 30
   _30 minutes_
   
   **begin_time** : HHMM - determines begin hour entity may be activated.
    
    --begin_time 0900
   _9:00 am_
   
   **end_time** : HHMM - determines end hour when entity is no longer allowed to activate.
    
    --end_time 2359    
   _11:59 pm_
   
   **begin_date** : YYYYMMDD - determines date when entity may be activated.
    
    --begin_date 20150101    
   _Jan 1, 2015_
   
   **end_date** : YYMMDD - indicates latest date entity may be activated.
    
    --end_date 20191231
   _Dec 31, 2019_
   
   **begin_lock_date** : YYYYMMDD - determines beginning of enforced inactive status
    
    --begin_lock_date 20180602
   _Jun 2, 2018_
   
   **end_lock_date** : YYMMDD - determines end of enforced inactive status.
    
    --end_lock_date 20180610
   _Jun 10, 2018_
   
   **day_mask** : 1234567, 1 = Sunday, 2 = Monday, etc - specifies which day of week entity may be activated.
    
    --day_mask 1246   
   _Sun, Mon, Wed, Fri_

   **all together**
   
    user mod --uid someuser --name anysafetext --timeout 30 --begin_time 0900 --end_time 2359 --begin_date 20150101 --end_date 20191231 --begin_lock_date 20180602 --end_lock_date 20180610 --day_mask 1246
    role add --name manager --description 'manager works 8-5, M-F' --timeout 10 --begin_time 0800 --end_time 1700 --begin_date 20100101 --end_date none --day_mask 1246
   _Constraints are optional and may be applied to user and role entities on add and mod operations_
   
### A Few Tips More

   * These commands have a one-to-one mapping to the admin and review APIs.  For example, the perm grant command maps to the admin.grant function and perm search –uid calls review.user_perms.
   * The description of the commands, including required arguments, can be inferred via the api doc inline to the admin and review modules.
   * The program output echos the inputted arguments and the results.
   
3. [AdminMgr](src/impl/admin.py) Examples:

    a. user add
    ````
    $ cli user add --uid 'chorowitz' --password 'secret' --description 'added with py-fortress cli'
    uid=chorowitz
    description=added with py-fortress cli
    user add
    success
    ````
    b. user mod
    ````
    $ cli user mod --uid 'chorowitz' --l 'my location' --ou 'my-ou' --department_number 123
    uid=chorowitz
    department_number=123
    l=my location
    ou=my-ou
    user mod
    success
    ````
    c. user del
    ````
    $ cli user del --uid 'chorowitz'
    uid=chorowitz
    user del
    success    
    ````
    d. user assign
    ````
    $ cli user assign --uid 'chorowitz' --role 'account-mgr'
    uid=chorowitz
    role name=account-mgr
    user assign
    success
    ````
    e. user deassign
    ````
    $ cli user deassign --uid 'chorowitz' --role 'account-mgr'
    uid=chorowitz
    role name=account-mgr
    user deassign
    success    
    ````
    f. role add
    ````
    $ cli role add --name 'account-mgr'
    name=account-mgr
    role add
    success
    ````
    g. role mod
    ````
    $ cli role mod --name 'account-mgr' --description 'this desc is optional'
    description=cli test role
    name=account-mgr
    role mod
    success    
    ````
    h. role del
    ````
    $ cli role del --name 'account-mgr'
    name=account-mgr
    process_role,delete
    success    
    ````
    i. object add
    ````
    $ cli object add --obj_name page456
    obj_name=page456
    object add
    success
    ````
    j. object mod
    ````
    $ cli object mod --obj_name page456 --description 'optional arg' --ou 'another optional arg'
    obj_name=page456
    ou=another optional arg
    description=optional arg
    object mod
    success
    ````
    k. object del
    ````
    $ cli object del --obj_name page789
    obj_name=page789
    object del
    success
    ````
    l. perm add
    ````
    $ cli perm add --obj_name page456 --op_name read
    obj_name=page456
    op_name=read
    perm add
    success
    ````
    m. perm mod
    ````
    $ cli perm mod --obj_name page456 --op_name read --description 'useful for human readable perm name'
    obj_name=page456
    op_name=read
    description=useful for human readable perm name
    perm mod
    success    
    ````
    n. perm del
    ````
    $ cli perm del --obj_name page456 --op_name search
    obj_name=page456
    op_name=search
    perm del
    success
    ````
    o. perm grant
    ````
    $ cli perm grant --obj_name page456 --op_name update --role account-mgr
    obj_name=page456
    op_name=update
    role name=account-mgr
    perm grant
    success
    ````
    p. perm revoke
    ````
    $ cli perm revoke --obj_name page456 --op_name update --role account-mgr
    obj_name=page456
    op_name=update
    role name=account-mgr
    perm revoke
    success    
    ````
    
4. [ReviewMgr](src/impl/review.py) Examples:

    a. user read 
    ````
    $ cli user read --uid chorowitz
    uid=chorowitz
    user read
    chorowitz
        uid: chorowitz
        dn: uid=chorowitz,ou=People,dc=example,dc=com  
        roles: ['account-mgr']              
        ...
    *************** chorowitz *******************
    success
    ````
    b. user search 
    ````
    $ cli user search --uid c
    uid=c
    user search
    c*:0
        uid: canders
        dn: uid=canders,ou=People,dc=example,dc=com
        roles: ['csr', 'tester']                
        ...
    *************** c*:0 *******************
    c*:1
        uid: cedwards
        dn: uid=cedwards,ou=People,dc=example,dc=com
        roles: ['manager', 'trainer']        
        ...
        
    *************** c*:1 *******************
    c*:2
        uid: chandler
        dn: uid=chandler,ou=People,dc=example,dc=com
        roles: ['auditor']        
        ...
    *************** c*:2 *******************
    c*:3
        uid: chorowitz
        dn: uid=chorowitz,ou=People,dc=example,dc=com
        roles: ['account-mgr']        
        ...
    *************** c*:3 *******************        
    success                                 
    ````
    c. role read 
    ````
    $ cli role read --name account-mgr
    name=account-mgr
    role read
    account-mgr
        dn: cn=account-mgr,ou=Roles,dc=example,dc=com
        members: ['uid=cli-user2,ou=People,dc=example,dc=com', 'uid=chorowitz,ou=People,dc=example,dc=com']
        internal_id: 5c189235-41b5-4e59-9d80-dfd64d16372c
        name: account-mgr
        constraint: <model.constraint.Constraint object at 0x7fc250bd9e10>
    Role Constraint:
            raw: account-mgr$0$$$$$$$
            timeout: 0
            name: account-mgr
    *************** account-mgr *******************
    success
    ````
    d. role search 
    ````
    $ cli role search --name py-
    name=py-
    role search
    py-*:0
        dn: cn=py-role-0,ou=Roles,dc=example,dc=com
        description: py-role-0 Role
        constraint: <model.constraint.Constraint object at 0x7f17e8745f60>
        members: ['uid=py-user-0,ou=People,dc=example,dc=com', 'uid=py-user-1,ou=People,dc=example,dc=com', ... ]
        internal_id: 04b82ce3-974b-4ff5-ad21-b19ecca57722
        name: py-role-0
    *************** py-*:0 *******************
    py-*:1
        dn: cn=py-role-1,ou=Roles,dc=example,dc=com
        description: py-role-1 Role
        constraint: <model.constraint.Constraint object at 0x7f17e8733128>
        members: ['uid=py-user-8,ou=People,dc=example,dc=com', 'uid=py-user-9,ou=People,dc=example,dc=com']
        internal_id: 70524da8-3be6-4372-a606-d8175e2ca63b
        name: py-role-1 
    *************** py-*:1 *******************
    py-*:2
        dn: cn=py-role-2,ou=Roles,dc=example,dc=com
        description: py-role-2 Role
        constraint: <model.constraint.Constraint object at 0x7f17e87332b0>
        members: ['uid=py-user-3,ou=People,dc=example,dc=com', 'uid=py-user-5,ou=People,dc=example,dc=com', 'uid=py-user-7,ou=People,dc=example,dc=com']
        internal_id: d1b9da70-9302-46c3-b21b-0fc45b863155
        name: py-role-2
    *************** py-*:2 *******************
    ...
    success
    ````
    e. object read 
    ````
    $ cli object read --obj_name page456
    obj_name=page456
    object read
    page456
        description: optional arg
        dn: ftObjNm=page456,ou=Perms,dc=example,dc=com
        internal_id: 1635cb3b-d5e2-4fcb-b61a-b8e91437e536
        obj_name: page456
        ou: another optional arg
    success
    ````
    f. object search 
    ````
    $ cli object search --obj_name page
    obj_name=page
    object search
    page*:0
        obj_name: page456
        description: optional arg
        dn: ftObjNm=page456,ou=Perms,dc=example,dc=com
        ou: another optional arg
        internal_id: 1635cb3b-d5e2-4fcb-b61a-b8e91437e536
    page*:1
        obj_name: page123
        description: optional arg
        dn: ftObjNm=page123,ou=Perms,dc=example,dc=com
        ou: another optional arg
        internal_id: a823ef98-7be4-4f49-a805-83bfef5a0dfb
    success
    ````
    g. perm read 
    ````
    $ cli perm read --obj_name page456 --op_name read
    op_name=read
    obj_name=page456
    perm read
    page456.read
        internal_id: 0dc55181-968e-4c60-8755-e20fa1ce017d
        dn: ftOpNm=read,ftObjNm=page456,ou=Perms,dc=example,dc=com
        abstract_name: page456.read
        description: useful for human readable perm name
        obj_name: page456
        op_name: read
    success    
    ````
    h. perm search
    ````
    $ cli perm search --obj_name page
    obj_name=page
    perm search
    page*.*:0
        abstract_name: page456.read
        op_name: read
        internal_id: 0dc55181-968e-4c60-8755-e20fa1ce017d
        obj_name: page456
        dn: ftOpNm=read,ftObjNm=page456,ou=Perms,dc=example,dc=com
        description: useful for human readable perm name
    page*.*:1
        roles: ['account-mgr']
        abstract_name: page456.update
        op_name: update
        internal_id: 626bca86-014b-4186-83a6-a583e39868a1
        obj_name: page456
        dn: ftOpNm=update,ftObjNm=page456,ou=Perms,dc=example,dc=com
    page*.*:2
        roles: ['account-mgr']
        abstract_name: page456.delete
        op_name: delete
        internal_id: 6c2fa5fc-d7c3-4e85-ba7f-5e514ca4263f
        obj_name: page456
        dn: ftOpNm=delete,ftObjNm=page456,ou=Perms,dc=example,dc=com
    success    
    ````
    i. perm search (by role) 
    ````
    $ cli perm search --role account-mgr
    perm search
    account-mgr:0
        abstract_name: page456.update
        obj_name: page456
        op_name: update
        roles: ['account-mgr']
        dn: ftOpNm=update,ftObjNm=page456,ou=Perms,dc=example,dc=com
        internal_id: 626bca86-014b-4186-83a6-a583e39868a1
    account-mgr:1
        abstract_name: page456.delete
        obj_name: page456
        op_name: delete
        roles: ['account-mgr']
        dn: ftOpNm=delete,ftObjNm=page456,ou=Perms,dc=example,dc=com
        internal_id: 6c2fa5fc-d7c3-4e85-ba7f-5e514ca4263f
    success
    ````
    j. perm search (by user)
    ````
    $ cli perm search --uid chorowitz
    perm search
    chorowitz:0
        dn: ftOpNm=update,ftObjNm=page456,ou=Perms,dc=example,dc=com
        internal_id: 626bca86-014b-4186-83a6-a583e39868a1
        roles: ['account-mgr']
        abstract_name: page456.update
        obj_name: page456
        op_name: update
    chorowitz:1
        dn: ftOpNm=delete,ftObjNm=page456,ou=Perms,dc=example,dc=com
        internal_id: 6c2fa5fc-d7c3-4e85-ba7f-5e514ca4263f
        roles: ['account-mgr']
        abstract_name: page456.delete
        obj_name: page456
        op_name: delete
    success
    ````
    
#### End of README-CLI