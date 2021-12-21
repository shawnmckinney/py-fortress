'''
@copyright: 2022 - Symas Corporation
'''

import unittest
import inspect

from rbac import (
    # model
    User,
    Role,
    Perm,
    PermObj,
    # apis:
    review,
    admin,
    access,
    #exception handling:
    RbacError,
    global_ids
)


class BasicTestSuite(unittest.TestCase):
    """These tests the py-fortress review functions."""
                

class TestSamples(unittest.TestCase):
    """
    Basic tests for beginners
    """    

    def test22_read_user(self):
        """
        Read a user that was created earlier. Expects a unique uid that points to an existing user.
        """
        print_test_name()
        try:
            out_user = review.read_user(User(uid='foo1'))
            print_user(out_user)
        except RbacError as e:            
            print_exception(e)
            self.fail()


    def test23_search_users(self):
        """
        Search for users that match the characters passed into with wildcard appended.  Will return zero or more records, one for each user in result set.
        """
        print_test_name()
        try:
            users = review.find_users(User(uid='foo*'))
            for user in users:
                print_user(user)
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test24_assigned_users(self):
        """
        Search for users that are assigned a particular role.  Will return zero or more records, one for each user in result set.
        """
        print_test_name()
        try:
            uids = review.assigned_users(Role(name='Customer'))
            for uid in uids:
                print_test_msg('uid=' + uid)
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test25_perm_users(self):
        """
        Search for users that have been authorized a particular permission.  Will return zero or more records, of type user, one for each user authorized that particular perm.
        """
        print_test_name()
        try:
            users = review.perm_users(Perm(obj_name='ShoppingCart', op_name='add'))
            for user in users:
                print_user(user)
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test10_add_user(self):
        """
        To add a user in py-fortress, the uid must be supplied.  All other attributes are optional but to be able to authenticate a password must be present of course.
        """
        print_test_name()
        
        try:
            admin.add_user(User(uid='foo1', password='secret'))
            print_test_msg('success')                        
        except RbacError as e:
            print_exception(e)
            self.fail()

    def test01_delete_user(self):
        """
        The delete expects the uid passed in to match one record only and will throw an exception if not found, or otherwise if error occurs.
        """
        print_test_name()
        try:
            admin.delete_user(User(uid='foo1'))
            print_test_msg('success')           
        except RbacError as e:
            if e.id == global_ids.USER_NOT_FOUND:
                print_test_msg('not found')
                pass
            else:
                print_exception(e)
                self.fail()


    def test12_read_role(self):
        """
        The read role expects the role name to point to an existing entry and will throw an exception if not found or other error occurs.
        """
        print_test_name()        
        try:
            out_role = review.read_role(Role(name='Customer'))
            print_role(out_role)                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test14_search_roles(self):
        """
        Search for roles that match the characters passed into with wildcard appended.  Will return zero or more records, one for each user in result set.
        """
        print_test_name()        
        try:
            roles = review.find_roles(Role(name='Customer*'))
            for role in roles:
                print_role(role)                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test15_assigned_roles(self):
        """
        Return the list of roles that have been assigned a particular user.  Will return zero or more records, of type constraint, one for each role assigned to user.
        """
        print_test_name()        
        try:
            constraints = review.assigned_roles(User(uid='foo1'))
            for constraint in constraints:
                print_test_msg('role name=' + constraint.name)                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test16_perm_roles(self):
        """
        Return the list of roles that have granted a particular perm.  Will return zero or more records, containing the role names, one for each role assigned to permission.
        """
        print_test_name()        
        try:
            names = review.perm_roles(Perm(obj_name='ShoppingCart', op_name='add'))
            for name in names:
                print_test_msg('role name=' + name)                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test08_add_role(self):
        """
        A fortress role only need to be supplied a name but it must be unique, and not present.
        """
        print_test_name()        
        try:
            admin.add_role(Role(name='Customer'))
            print_test_msg('success')                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test05_delete_role(self):
        """
        The delete will throw an exception if the passed role is not found or otherwise fails to process.
        """
        print_test_name()        
        try:
            admin.delete_role(Role(name='Customer'))
            print('test5_delete_role success')
        except RbacError as e:
            if e.id == global_ids.ROLE_NOT_FOUND:
                print('test5_delete_role not found')
                pass
            else:            
                print_exception(e)
                self.fail()


    def test13_read_obj(self):
        """
        The ob_name is the only required attribute on a fortress object. Will throw an exception if not found.
        """
        print_test_name()        
        try:
            out_obj = review.read_object(PermObj(obj_name='ShoppingCart'))
            print_obj(out_obj)                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test17_search_objs(self):
        """
        Search for ojects that match the characters passed into with wildcard appended.  Will return zero or more records, one for each user in result set.
        """
        print_test_name()        
        try:
            objs = review.find_objects(PermObj(obj_name='ShoppingCart*'))
            for obj in objs:
                print_obj(obj)                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test06_add_obj(self):
        """
        The ob_name is the only required attribute on a fortress object. Will throw an exception if not unique.
        """
        print_test_name()
        
        try:
            admin.add_object(PermObj(obj_name='ShoppingCart'))
            print_test_msg('success')                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test04_delete_obj(self):
        """
        Delete a basic perm object
        """
        print_test_name()
        
        try:
            admin.delete_object(PermObj(obj_name='ShoppingCart'))
            print_test_msg('success')                        
        except RbacError as e:
            if e.id == global_ids.PERM_OBJ_NOT_FOUND:
                print_test_msg('obj not found')
                pass
            else:            
                print_exception(e)
                self.fail()


    def test18_read_perm(self):
        """
        Permissions require obj_name and op_name, obj_id is optional.  This will throw an exception if not found.
        """
        print_test_name()        
        try:
            out_perm = review.read_perm(Perm(obj_name='ShoppingCart', op_name='add'))
            print_perm(out_perm)                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test19_search_perms(self):
        """
        Search for perms that match the characters passed into with wildcard appended.  Will return zero or more records, one for each user in result set.
        """
        print_test_name()        
        try:
            perms = review.find_perms(Perm(obj_name='ShoppingCart*', op_name='*'))
            for perm in perms:
                print_perm(perm)                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test20_role_perms(self):
        """
        Search for perms that have been granted to a particular role.  Will return zero or more records, of type permission, one for each grant.
        """
        print_test_name()        
        try:
            perms = review.role_perms(Role(name='Customer'))
            for perm in perms:
                print_perm(perm)                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test21_user_perms(self):
        """
        Search for perms that have been authorized to a particular user based on their role assignments.  Will return zero or more records, of type permission, one for each perm authorized for user.
        """
        print_test_name()        
        try:
            perms = review.user_perms(User(uid='foo1'))
            for perm in perms:
                print_perm(perm)                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test07_add_perm(self):
        """
        Permissions require obj_name and op_name, obj_id is optional.  This will throw an exception if not unique.
        """
        print_test_name()
        
        try:
            admin.add_perm(Perm(obj_name='ShoppingCart', op_name='add'))
            print_test_msg('success')                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test03_delete_perm(self):
        """
        Permissions require obj_name and op_name, obj_id is optional.  This will throw an exception if not found.
        """
        print('test3_delete_perm')
        try:
            admin.delete_perm(Perm(obj_name='ShoppingCart', op_name='add'))
            print_test_msg('success')                        
        except RbacError as e:
            if e.id == global_ids.PERM_OP_NOT_FOUND:
                print_test_msg('not found')
                pass
            else:            
                print_exception(e)
                self.fail()


    def test09_grant_perm(self):
        """
        Grant a permission to a role passing required attrs for perm (obj_name op_name) and role (name). Throws exception if perm not found, or already have been granted.
        """
        print_test_name()
        
        try:
            admin.grant(Perm(obj_name='ShoppingCart', op_name='add'), Role(name="Customer"))
            print_test_msg('success')                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test02_revoke_perm(self):
        """
        Revokes a permission from a role passing required attrs for perm (obj_name op_name) and role (name). Throws exception if perm not found, or if not granted.
        """
        print_test_name()
        
        try:
            admin.revoke(Perm(obj_name='ShoppingCart', op_name='add'), Role(name="Customer"))
            print_test_msg('success')                        
        except RbacError as e:
            if e.id == global_ids.PERM_NOT_EXIST:
                print_test_msg('not granted')
            else:
                print_exception(e)
                self.fail()


    def test11_assign_user(self):
        """
        Assign a user to a role passing req's attrs for user (uid) and role (name). Throws exception if either are not found, or already assigned.
        """
        print_test_name()
        
        try:
            admin.assign(User(uid='foo1'), Role(name='Customer'))
            print_test_msg('success')                        
        except RbacError as e:
            print_exception(e)
            self.fail()


    def test26_create_session(self):
        """
        Called when beginning an RBAC session. Requires uid and password if trusted is False, in which case it will authenticate in addition to activating roles into session.
        Throws exception if user is not found, or if authentication fails. 
        """
        print_test_name()
        
        try:
            session = access.create_session(User(uid='foo1', password='secret'), False)
            if not session:
                print_test_msg('fail')
                self.fail()
            else:
                print_test_msg('sucess')
                pass                        
        except RbacError as e:
            print_exception(e)
            self.fail()
                        

    def test27_check_access(self):
        """
        Called to perform an RBAC permmission check.  Requires a valid session (returned from create_session) and a permission with required attrs obj_name, op_name, and optional obj_id.
        Returns true if user is allowed to perform the specified operation on object.
        """
        print_test_name()
        
        try:
            session = access.create_session(User(uid='foo1', password='secret'), False)
            result = access.check_access(session, Perm(obj_name='ShoppingCart', op_name='add'))
            if not result:
                print_test_msg('fail')
                self.fail()
            else:
                print_test_msg('success')
                pass                        
        except RbacError as e:
            print_exception(e)
            self.fail()
                        

    def test28_session_perms(self):
        """
        Return all permission authorized for user per their set of activated roles in the session.  Note this means that set could be a subset of assigned permissions, if any assigned roles are not activated.
        """
        print_test_name()
        
        try:
            session = access.create_session(User(uid='foo1', password='secret'), False)
            perms = access.session_perms(session)
            if not perms:
                print_test_msg('failed')
                self.fail()
            
            for perm in perms:
                print_perm(perm)
            pass                        
        except RbacError as e:
            print_exception(e)
            self.fail()
            
            
def print_test_name(): 
    print(inspect.currentframe().f_back.f_code.co_name)
        

def print_test_msg(msg=None):
    if msg is None:
        msg = '' 
    print(inspect.currentframe().f_back.f_code.co_name + ' ' + msg)
        

def print_exception(e):
    print(inspect.currentframe().f_back.f_code.co_name + ' exception id=' + str(e.id) + ', msg=' + e.msg)
        

def print_user (entity):
        caller = inspect.currentframe().f_back.f_code.co_name
        print(caller + ' uid:' + entity.uid)

        
def print_role (entity):
        caller = inspect.currentframe().f_back.f_code.co_name
        print(caller + ' role name:' + entity.name)


def print_obj (entity):
        caller = inspect.currentframe().f_back.f_code.co_name
        print(caller + ' object name:' + entity.obj_name)


def print_perm (entity):
        caller = inspect.currentframe().f_back.f_code.co_name
        print(caller + ' object name:' + entity.obj_name + ' op name:' + entity.op_name)    
        
        
def suite():
    suite = unittest.TestSuite()

    # Teardown:        
    suite.addTest(TestSamples('test01_delete_user'))
    suite.addTest(TestSamples('test02_revoke_perm'))
    suite.addTest(TestSamples('test03_delete_perm'))
    suite.addTest(TestSamples('test04_delete_obj'))
    suite.addTest(TestSamples('test05_delete_role'))
        
    # Buildup:
    suite.addTest(TestSamples('test06_add_obj'))
    suite.addTest(TestSamples('test07_add_perm'))
    suite.addTest(TestSamples('test08_add_role'))
    suite.addTest(TestSamples('test09_grant_perm'))
    suite.addTest(TestSamples('test10_add_user'))
    suite.addTest(TestSamples('test11_assign_user'))

    # Interrogate entities and their relationships:
    suite.addTest(TestSamples('test12_read_role'))
    suite.addTest(TestSamples('test13_read_obj'))
    suite.addTest(TestSamples('test14_search_roles'))
    suite.addTest(TestSamples('test15_assigned_roles'))
    suite.addTest(TestSamples('test16_perm_roles'))
    suite.addTest(TestSamples('test17_search_objs'))
    suite.addTest(TestSamples('test18_read_perm'))
    suite.addTest(TestSamples('test19_search_perms'))
    suite.addTest(TestSamples('test20_role_perms'))
    suite.addTest(TestSamples('test21_user_perms'))
    suite.addTest(TestSamples('test22_read_user'))
    suite.addTest(TestSamples('test23_search_users'))
    suite.addTest(TestSamples('test24_assigned_users'))
    suite.addTest(TestSamples('test25_perm_users'))
    
    # Test the policies:    
    suite.addTest(TestSamples('test26_create_session'))
    suite.addTest(TestSamples('test27_check_access'))
    suite.addTest(TestSamples('test28_session_perms'))
    return suite  
 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())