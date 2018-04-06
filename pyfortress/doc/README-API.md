# py-fortress API Usage Guide
 
RBAC0 APIs
_____________________________________________________________________________
## Table of Contents
 * SECTION 1. Introduction 
 * SECTION 2. Prerequisites
 * SECTION 3. Usage
___________________________________________________________________________________
## SECTION 1. Introduction

There are about 26 APIs currently in [admin_mgr](../impl/admin_mgr.py), [review_mgr](../impl/review_mgr.py) and [access_mgr](../impl/access_mgr.py).
This guide doesn't yet cover them all.
______________________________________________________________________________
## SECTION 2. Prerequisites

1. Completed SECTION 2. *Start using ApacheDS or OpenLDAP Docker Image*: [README-QUICKSTART](.README-QUICKSTART.md)
2. Completed: [README-INSTALL](.README-INSTALL.md)
3. Copied [py-fortress-cfg.json](test/py-fortress-cfg.json) to the runtime folder of your python program, correctly pointing to an LDAP server (per step 1 above).

* The [py-fortress-sample](https://github.com/shawnmckinney/py-fortress-sample) project has an example of how to setup a test program you can use as a starting point.    ___________________________________________________________________________________
______________________________________________________________________________
## SECTION 3. Usage

0. Prepare your python module for usage by importing:

    ```
    from pyfortress import (
        # model
        User,
        Role,
        Perm,
        PermObj,
        # apis:
        review_mgr, 
        admin_mgr, 
        access_mgr,
        #exception handling:
        FortressError,
        global_ids
    )
    ```

1. Add a user:

    ```
    def test_add_user(self):
        """
        Add a basic user
        """
        print('test_add_user')
        
        try:
            admin_mgr.add_user(User(uid='foo1', password='secret'))
            print('test_add_user success')                        
        except FortressError as e:
            self.fail('test_add_user failed, exception=' + e.msg)     
    ```

2. Add a role:

    ```
    def test_add_role(self):
        """
        Add a basic role
        """
        print('test_add_role')        
        try:
            admin_mgr.add_role(Role(name='Customer'))
            print('test_add_role success')                        
        except FortressError as e:
            self.fail('test_add_role failed, exception=' + e.msg)     
    ```

3. Add an object:

    ```
    def test_add_obj(self):
        """
        Add a basic perm object
        """
        print('test_add_obj')
        
        try:
            admin_mgr.add_object(PermObj(obj_name='ShoppingCart'))
            print('test_add_obj success')                        
        except FortressError as e:
            self.fail('test_add_obj failed, exception=' + e.msg)     
    ```


4. Add a perm:

    ```
    def test_add_perm(self):
        """
        Add a basic perm
        """
        print('test_add_perm')
        
        try:
            admin_mgr.add_perm(Perm(obj_name='ShoppingCart', op_name='add'))
            print('test_add_perm success')                        
        except FortressError as e:
            self.fail('test_add_perm failed, exception=' + e.msg)     
    ```

5. Assign a user:

    ```
    def test_assign_user(self):
        """
        Assign a user to a role
        """
        print('test_assign_user')
        
        try:
            admin_mgr.assign(User(uid='foo1'), Role(name='Customer'))
            print('test_assign_user success')                        
        except FortressError as e:
            self.fail('test_assign_user failed, exception=' + e.msg)     
    ```

6. Grant a permission:

    ```
    def test_grant_perm(self):
        """
        Grant a permission to a role
        """
        print('test_grant_perm')
        
        try:
            admin_mgr.grant(Perm(obj_name='ShoppingCart', op_name='add'), Role(name="Customer"))
            print('test_grant_perm success')                        
        except FortressError as e:
            self.fail('test_grant_perm failed, exception=' + e.msg)     
    ```

7. Now test signing on the RBAC way:

    ```
    def test_create_session(self):
        """
        create session
        """
        print('test_create_session')
        
        try:
            session = access_mgr.create_session(User(uid='foo1', password='secret'), False)
            if not session:
                print('test_create_session fail')
                self.fail('test_create_session fail')
            else:
                print('test_create_session pass')
                pass                        
        except FortressError as e:
            self.fail('test_create_session failed, exception=' + e.msg)            
    ```
    
    _The session will then be held on to by the client for subsequent calls like check_access and session_perms_

8. Here's how to check a single permission:

    ```
    def test_check_access(self):
        """
        create session and check perm
        """
        print('test_check_access')
        
        try:
            session = ... obtained earlier
            result = access_mgr.check_access(session, Perm(obj_name='ShoppingCart', op_name='add'))
            if not result:
                print('test_check_access fail')
                self.fail('test_check_access fail')
            else:
                print('test_check_access pass')
                pass                        
        except FortressError as e:
            self.fail('test_check_access failed, exception=' + e.msg)                 
    ```

9. Retrieve all of the permissions as a list:

    ```
    def test_session_perms(self):
        """
        create session and get perms for user
        """
        print('test_check_access')
        
        try:
            session = ... obtained earlier
            perms = access_mgr.session_perms(session)
            if not perms:
                print('test_session_perms failed')
                self.fail('test_session_perms failed')
            
            for perm in perms:
                print_perm(perm, 'session_perms: ')
            pass                        
        except FortressError as e:
            self.fail('test_session_perms failed, exception=' + e.msg)     
    ```

10. More... [py-fortress-sample](https://github.com/shawnmckinney/py-fortress-sample)