# py-fortress Command Line Interpreter (CLI) README 

-------------------------------------------------------------------------------
## Table of Contents
 * SECTION 1. Introduction 
 * SECTION 2. Prerequisites
 * SECTION 3. Run it
___________________________________________________________________________________
## SECTION 1. Introduction

The py-fortress CLI drive the [admin_mgr](impl/admin_mgr.py) and [review_mgr](impl/review_mgr.py) APIs.
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
    * read
    * search
    
    The args are '--' + names contained within the py-fortress entities:
    * [user](model/user.py)
    * [role](model/role.py)
    * [object](model/object.py)
    * [perm](model/pern.py)
    
    Tips:
    * These commands follow exact same rules as the [admin_mgr](impl/admin_mgr.py) and [review_mgr](impl/review_mgr.py) APIs.  To understand usage, including required arguments, view its inline code doc.
    * The output will echo the arguments and result.
    * user and perm entities require the *--role* arg for *assign*, *deassign*, *grant*, and *revoke* operations
    
3. AdminMgr Examples [admin_mgr](impl/admin_mgr.py):

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
    
4. ReviewMgr Examples [review_mgr](impl/review_mgr.py):

    a. user read 
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py user read --uid chorowitz
    uid=chorowitz
    user read
    chorowitz
        pw_policy: 
        cn: chorowitz
        uid: chorowitz
        ...
    *************** chorowitz *******************
    success
    ````
    b. user search 
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py user search --uid c
    uid=c
    user search
    c*:0
        uid: cli-user1
        dn: uid=cli-user1,ou=People,dc=example,dc=com
        ...
    *************** c*:0 *******************
    c*:1
        uid: cli-user2
        dn: uid=cli-user2,ou=People,dc=example,dc=com
        ...
        
    *************** c*:1 *******************
    c*:2
        uid: cli-user3
        dn: uid=cli-user3,ou=People,dc=example,dc=com
        ...
    *************** c*:2 *******************
    c*:3
        uid: chorowitz
        dn: uid=chorowitz,ou=People,dc=example,dc=com
        ...
    *************** c*:3 *******************        
    success                                 
    ````
    c. role read 
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py role read --name account-mgr
    name=account-mgr
    role read
    account-mgr
        dn: cn=account-mgr,ou=Roles,dc=example,dc=com
        props: 
        members: ['uid=cli-user2,ou=People,dc=example,dc=com', 'uid=chorowitz,ou=People,dc=example,dc=com']
        internal_id: 5c189235-41b5-4e59-9d80-dfd64d16372c
        name: account-mgr
        constraint: <model.constraint.Constraint object at 0x7fc250bd9e10>
        description: 
    Role Constraint:
            raw: account-mgr$0$$$$$$$
            end_date: 
            end_lock_date: 
            timeout: 0
            begin_time: 
            end_time: 
            name: account-mgr
            day_mask: 
            begin_date: 
            begin_lock_date: 
    *************** account-mgr *******************
    success
    ````
    d. role search 
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py role search --name py-
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
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py object read --obj_name page456
    obj_name=page456
    object read
    page456
        description: optional arg
        dn: ftObjNm=page456,ou=Perms,dc=example,dc=com
        internal_id: 1635cb3b-d5e2-4fcb-b61a-b8e91437e536
        props: 
        obj_name: page456
        ou: another optional arg
        type: 
    success
    ````
    f. object search 
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py object search --obj_name page
    obj_name=page
    object search
    page*:0
        props: 
        obj_name: page456
        description: optional arg
        dn: ftObjNm=page456,ou=Perms,dc=example,dc=com
        ou: another optional arg
        type: 
        internal_id: 1635cb3b-d5e2-4fcb-b61a-b8e91437e536
    page*:1
        props: 
        obj_name: page123
        description: optional arg
        dn: ftObjNm=page123,ou=Perms,dc=example,dc=com
        ou: another optional arg
        type: 
        internal_id: a823ef98-7be4-4f49-a805-83bfef5a0dfb
    success
    ````
    g. perm read 
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py perm read --obj_name page456 --op_name read
    op_name=read
    obj_name=page456
    perm read
    page456.read
        internal_id: 0dc55181-968e-4c60-8755-e20fa1ce017d
        dn: ftOpNm=read,ftObjNm=page456,ou=Perms,dc=example,dc=com
        abstract_name: page456.read
        type: 
        roles: 
        description: useful for human readable perm name
        props: 
        obj_name: page456
        obj_id: 
        op_name: read
        users: 
    success    
    ````
    h. perm search
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py perm search --obj_name page
    obj_name=page
    perm search
    page*.*:0
        props: 
        roles: 
        abstract_name: page456.read
        obj_id: 
        users: 
        op_name: read
        internal_id: 0dc55181-968e-4c60-8755-e20fa1ce017d
        obj_name: page456
        type: 
        dn: ftOpNm=read,ftObjNm=page456,ou=Perms,dc=example,dc=com
        description: useful for human readable perm name
    page*.*:1
        props: 
        roles: ['account-mgr']
        abstract_name: page456.update
        obj_id: 
        users: 
        op_name: update
        internal_id: 626bca86-014b-4186-83a6-a583e39868a1
        obj_name: page456
        type: 
        dn: ftOpNm=update,ftObjNm=page456,ou=Perms,dc=example,dc=com
        description: 
    page*.*:2
        props: 
        roles: ['account-mgr']
        abstract_name: page456.delete
        obj_id: 
        users: 
        op_name: delete
        internal_id: 6c2fa5fc-d7c3-4e85-ba7f-5e514ca4263f
        obj_name: page456
        type: 
        dn: ftOpNm=delete,ftObjNm=page456,ou=Perms,dc=example,dc=com
        description: 
    success    
    ````
    i. perm search (by role) 
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py perm search --role account-mgr
    perm search
    account-mgr:0
        description: 
        abstract_name: page456.update
        obj_id: 
        obj_name: page456
        users: 
        op_name: update
        type: 
        props: 
        roles: ['account-mgr']
        dn: ftOpNm=update,ftObjNm=page456,ou=Perms,dc=example,dc=com
        internal_id: 626bca86-014b-4186-83a6-a583e39868a1
    account-mgr:1
        description: 
        abstract_name: page456.delete
        obj_id: 
        obj_name: page456
        users: 
        op_name: delete
        type: 
        props: 
        roles: ['account-mgr']
        dn: ftOpNm=delete,ftObjNm=page456,ou=Perms,dc=example,dc=com
        internal_id: 6c2fa5fc-d7c3-4e85-ba7f-5e514ca4263f
    success
    ````
    j. perm search (by user)
    ````
    (env)~/GIT/pyDev/py-fortress/test$ python3 cli.py perm search --uid chorowitz
    perm search
    chorowitz:0
        type: 
        description: 
        dn: ftOpNm=update,ftObjNm=page456,ou=Perms,dc=example,dc=com
        obj_id: 
        users: 
        internal_id: 626bca86-014b-4186-83a6-a583e39868a1
        roles: ['account-mgr']
        abstract_name: page456.update
        props: 
        obj_name: page456
        op_name: update
    chorowitz:1
        type: 
        description: 
        dn: ftOpNm=delete,ftObjNm=page456,ou=Perms,dc=example,dc=com
        obj_id: 
        users: 
        internal_id: 6c2fa5fc-d7c3-4e85-ba7f-5e514ca4263f
        roles: ['account-mgr']
        abstract_name: page456.delete
        props: 
        obj_name: page456
        op_name: delete
    success
    ````
### END OF README