'''
Created on Mar 19, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

import unittest
from impl import review_mgr, admin_mgr, access_mgr
from model import User, Role, Perm, PermObj
from util import global_ids
from test.utils import print_user, print_role, print_ln, print_entity
import user_test_data, role_test_data, perm_test_data


class BasicTestSuite(unittest.TestCase):
    """These tests the py-fortress review_mgr functions."""
                

class TestSamples(unittest.TestCase):
    """
    Basic tests for beginners
    """    

    def test_read_user(self):
        """
        Read a basic user
        """
        print_ln('test_read_user')
        
        try:
            out_user = review_mgr.read_user(User(uid='foo1'))
            print_user(out_user, 'test_read_user')
        except Exception as e:
            self.fail('test_read_user failed, exception=' + e.msg)


    def test_add_user(self):
        """
        Add a basic user
        """
        print_ln('test_add_user')
        
        try:
            admin_mgr.add_user(User(uid='foo1', password='secret'))
            print_ln('test_add_user success')                        
        except Exception as e:
            self.fail('test_add_user failed, exception=' + e.msg)


    def test_delete_user(self):
        """
        Delete the simple user
        """
        print_ln('test_delete_user')
        try:
            admin_mgr.delete_user(User(uid='foo1')) 
            print_ln('test_delete_user success')           
        except Exception as e:
            if e.id == global_ids.USER_NOT_FOUND:
                print_ln('test_delete_user not found')
                pass
            else:
                self.fail('test_delete_user failed, exception=' + e.msg)


    def test_read_role(self):
        """
        Read a basic role
        """
        print_ln('test_read_role')        
        try:
            out_role = review_mgr.read_role(Role(name='Customer'))
            print_role(out_role, 'test_read_role')                        
        except Exception as e:
            self.fail('test_read_role failed, exception=' + e.msg)


    def test_add_role(self):
        """
        Add a basic role
        """
        print_ln('test_add_role')        
        try:
            admin_mgr.add_role(Role(name='Customer'))
            print_ln('test_add_role success')                        
        except Exception as e:
            self.fail('test_add_role failed, exception=' + e.msg)


    def test_delete_role(self):
        """
        Delete a basic role
        """
        print_ln('test_delete_role')        
        try:
            admin_mgr.delete_role(Role(name='Customer'))
            print_ln('test_delete_role success')                        
        except Exception as e:
            if e.id == global_ids.ROLE_NOT_FOUND:
                print_ln('test_delete_role not found')
                pass
            else:            
                self.fail('test_delete_role failed, exception=' + e.msg)


    def test_read_obj(self):
        """
        Read a basic perm object
        """
        print_ln('test_read_obj')        
        try:
            out_obj = review_mgr.read_object(PermObj(obj_name='ShoppingCart'))
            print_entity(out_obj, 'test_read_obj')                        
        except Exception as e:
            self.fail('test_read_obj failed, exception=' + e.msg)


    def test_add_obj(self):
        """
        Add a basic perm object
        """
        print_ln('test_add_obj')
        
        try:
            admin_mgr.add_object(PermObj(obj_name='ShoppingCart'))
            print_ln('test_add_obj success')                        
        except Exception as e:
            self.fail('test_add_obj failed, exception=' + e.msg)


    def test_delete_obj(self):
        """
        Delete a basic perm object
        """
        print_ln('test_delete_obj')
        
        try:
            admin_mgr.delete_object(PermObj(obj_name='ShoppingCart'))
            print_ln('test_delete_obj success')                        
        except Exception as e:
            if e.id == global_ids.PERM_OBJ_NOT_FOUND:
                print_ln('test_delete_obj not found')
                pass
            else:            
                self.fail('test_delete_obj failed, exception=' + e.msg)


    def test_read_perm(self):
        """
        Read a basic perm
        """
        print_ln('test_read_perm')        
        try:
            out_perm = review_mgr.read_perm(Perm(obj_name='ShoppingCart', op_name='add'))
            print_entity(out_perm, 'test_read_perm')                        
        except Exception as e:
            self.fail('test_read_perm failed, exception=' + e.msg)


    def test_add_perm(self):
        """
        Add a basic perm
        """
        print_ln('test_add_perm')
        
        try:
            admin_mgr.add_perm(Perm(obj_name='ShoppingCart', op_name='add'))
            print_ln('test_add_perm success')                        
        except Exception as e:
            self.fail('test_add_perm failed, exception=' + e.msg)


    def test_delete_perm(self):
        """
        Delete a basic perm
        """
        print_ln('test_delete_perm')
        try:
            admin_mgr.delete_perm(Perm(obj_name='ShoppingCart', op_name='add'))
            print_ln('test_delete_perm success')                        
        except Exception as e:
            if e.id == global_ids.PERM_OP_NOT_FOUND:
                print_ln('test_delete_perm not found')
                pass
            else:            
                self.fail('test_delete_perm failed, exception=' + e.msg)


    def test_grant_perm(self):
        """
        Grant a permission to a role
        """
        print_ln('test_grant_perm')
        
        try:
            admin_mgr.grant(Perm(obj_name='ShoppingCart', op_name='add'), Role(name="Customer"))
            print_ln('test_grant_perm success')                        
        except Exception as e:
            self.fail('test_grant_perm failed, exception=' + e.msg)


    def test_revoke_perm(self):
        """
        Revoke a permission from a role
        """
        print_ln('test_revoke_perm')
        
        try:
            admin_mgr.revoke(Perm(obj_name='ShoppingCart', op_name='add'), Role(name="Customer"))
            print_ln('test_revoke_perm success')                        
        except Exception as e:
            if e.id == global_ids.PERM_ROLE_NOT_EXIST:
                print_ln('test_revoke_perm not granted')
            else:
                print_ln('test_revoke_perm error=' + e.msg)
                #self.fail('test_revoke_perm failed, exception=' + e.msg)


    def test_assign_user(self):
        """
        Assign a user to a role
        """
        print_ln('test_assign_user')
        
        try:
            admin_mgr.assign(User(uid='foo1'), Role(name='Customer'))
            print_ln('test_assign_user success')                        
        except Exception as e:
            self.fail('test_assign_user failed, exception=' + e.msg)


    def test_check_access(self):
        """
        create session and check perm
        """
        print_ln('test_check_access')
        
        try:
            session = access_mgr.create_session(User(uid='foo1', password='secret'), False)
            result = access_mgr.check_access(session, Perm(obj_name='ShoppingCart', op_name='add'))
            if not result:
                print_ln('test_check_access fail')
                self.fail('test_check_access fail')
            else:
                print_ln('test_check_access pass')
                pass                        
        except Exception as e:
            self.fail('test_check_access failed, exception=' + e.msg)


def suite():
    suite = unittest.TestSuite()
    
    # Teardown:        
    suite.addTest(TestSamples('test_delete_user'))
    suite.addTest(TestSamples('test_revoke_perm'))        
    suite.addTest(TestSamples('test_delete_perm'))        
    suite.addTest(TestSamples('test_delete_obj'))
    suite.addTest(TestSamples('test_delete_role'))
        
    # Buildup:
    suite.addTest(TestSamples('test_add_obj'))
    suite.addTest(TestSamples('test_add_perm'))
    suite.addTest(TestSamples('test_add_role'))    
    suite.addTest(TestSamples('test_grant_perm'))
    suite.addTest(TestSamples('test_add_user'))    
    suite.addTest(TestSamples('test_assign_user'))

    # Interrogate:
    suite.addTest(TestSamples('test_read_role'))    
    suite.addTest(TestSamples('test_read_obj'))
    suite.addTest(TestSamples('test_read_perm'))
    suite.addTest(TestSamples('test_read_user'))
    
    suite.addTest(TestSamples('test_check_access'))
    
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())