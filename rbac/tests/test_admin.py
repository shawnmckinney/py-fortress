'''
@copyright: 2022 - Symas Corporation
'''

import unittest
from rbac import admin, review
from rbac.model import User, Role, Perm, PermObj
from rbac.cli.utils import print_user, print_role, print_ln
from rbac.tests import user_test_data, role_test_data
from rbac.tests import perm_test_data


class BasicTestSuite(unittest.TestCase):
    """These tests the py-fortress admin functions."""
                

class TestAdminMgr(unittest.TestCase):
    """
    Test the admin funcs
    """    

    def test10_add_user(self):
        """
        Test the add user method
        """
        print_ln('test_add_user')
        usrs = user_test_data.get_test_users('py-user', 10)
        for usr in usrs:
            try:                        
                entity = admin.add_user(usr)
                print_user(entity, "Add User")
            except Exception as e:
                self.fail('test_add_user failed, exception=' + e.msg)


    def test05_delete_user(self):
        """
        Test the user delete user method
        """
        print_ln('test_delete_user')
        
        try:
            # TODO: search for roles assigned to user and remove the occupant
            uList = review.find_users(User(uid='py-user*'))
            for usr in uList:                       
                entity = admin.delete_user(usr)
                print_ln("Delete user=" + entity.uid)
        except Exception as e:
            self.fail('test_delete_user failed, exception=' + e.msg)


    def test07_add_role(self):
        """
        Test the add role method
        """
        print_ln('test_add_role')
        rles = role_test_data.get_test_roles('py-role', 10)
        for rle in rles:
            try:                        
                entity = admin.add_role(rle)
                print_role(entity, "Add Role")
            except Exception as e:
                self.fail('test_add_role failed, exception=' + e.msg)


    def test06_delete_role(self):
        """
        Test the role delete user method
        """
        print_ln('test_delete_role')
        
        try:
            rList = review.find_roles(Role(name='py-role*'))
            for rle in rList:                       
                entity = admin.delete_role(rle)
                print_ln("Delete role=" + entity.name)
        except Exception as e:
            self.fail('test_delete_role failed, exception=' + e.msg)


    def test08_add_object(self):
        """
        Test the add object method
        """
        print_ln('test_add_object')
        objs = perm_test_data.get_test_objs('py-obj', 10)
        for obj in objs:
            try:                        
                entity = admin.add_object(obj)
                print_ln("Add Object=" + entity.obj_name)                
            except Exception as e:
                self.fail('test_add_object failed, exception=' + e.msg)


    def test03_delete_object(self):
        """
        Test the role delete object method
        """
        print_ln('test_delete_object')
        
        try:
            oList = review.find_objects(PermObj(obj_name='py-obj*'))
            for obj in oList:                       
                admin.delete_object(obj)
                print_ln("Delete Object=" + obj.obj_name)
        except Exception as e:
            self.fail('test_delete_object failed, exception=' + e.msg)


    def test09_add_perm(self):
        """
        Test the add perm method
        """
        print_ln('test_add_perm')
        perms = perm_test_data.get_test_perms('py-obj', 10)
        for perm in perms:
            try:                        
                entity = admin.add_perm(perm)
                print_ln("Add Perm obj name=" + entity.obj_name + ', op=' + entity.op_name + ', id=' + entity.obj_id)                                
            except Exception as e:
                self.fail('test_add_perm failed, exception=' + e.msg)


    def test02_delete_perm(self):
        """
        Test the perm delete object method
        """
        print_ln('test_delete_perm')
        
        try:
            pList = review.find_perms(Perm(obj_name='py-obj*', op_name='*'))
            for perm in pList:                       
                entity = admin.delete_perm(perm)
                print_ln("Delete Perm obj name=" + entity.obj_name + ', op=' + entity.op_name + ', id=' + entity.obj_id)
        except Exception as e:
            self.fail('test_delete_perm failed, exception=' + e.msg)


    def test11_assign_user(self):
        """
        Test the assign user method
        """
        print_ln('test_assign_user')
        usrs = user_test_data.get_test_users('py-user', 10)
        rles = role_test_data.get_test_roles('py-role', 10)        
        for usr in usrs:
            for rle in rles:
                try:                        
                    admin.assign(usr, rle)
                    print_ln("Assign User=" + usr.uid + ', Role=' + rle.name)
                except Exception as e:
                    self.fail('test_assign_user failed, exception=' + e.msg)


    def test04_deassign_user(self):
        """
        Test the user deassign method
        """
        print_ln('test_deassign_user')
        
        try:
            uList = review.find_users(User(uid='py-user*'))
            rles = role_test_data.get_test_roles('py-role', 10)                
            for usr in uList:
                for rle in rles:                                       
                    entity = admin.deassign(usr, rle)
                    print_ln("Deassign User=" + entity.uid + ', Role=' + rle.name)
        except Exception as e:
            pass
            #self.fail('test_deassign_user failed, exception=' + e.msg)


    def test12_grant(self):
        """
        Test the grant method
        """
        print_ln('test_grant')
        perms = perm_test_data.get_test_perms('py-obj', 10)
        rles = role_test_data.get_test_roles('py-role', 10)        
        for perm in perms:
            for rle in rles:
                try:                        
                    admin.grant(perm, rle)
                    print_ln("Grant Perm obj name=" + perm.obj_name + ', op=' + perm.op_name + ', id=' + perm.obj_id + ', Role=' + rle.name)                                
                except Exception as e:
                    self.fail('test_grant failed, exception=' + e.msg)


    def test01_revoke(self):
        """
        Test the revoke method
        """
        print_ln('test_revoke')
        
        try:
            pList = review.find_perms(Perm(obj_name='py-obj*', op_name='*'))
            rles = role_test_data.get_test_roles('py-role', 10)                                    
            for perm in pList:                       
                for rle in rles:
                    admin.revoke(perm, rle)
                    print_ln("Revoke Perm obj name=" + perm.obj_name + ', op=' + perm.op_name + ', id=' + perm.obj_id + ', Role=' + rle.name)                                
        except Exception as e:
            pass
            #self.fail('test_revoke failed, exception=' + e.msg)


def suite():
    suite = unittest.TestSuite()
    
    # Teardown:
    suite.addTest(TestAdminMgr('test01_revoke'))
    suite.addTest(TestAdminMgr('test02_delete_perm'))
    suite.addTest(TestAdminMgr('test03_delete_object'))
    suite.addTest(TestAdminMgr('test04_deassign_user'))
    suite.addTest(TestAdminMgr('test05_delete_user'))
    suite.addTest(TestAdminMgr('test06_delete_role'))
    
    # Buildup:
    suite.addTest(TestAdminMgr('test07_add_role'))
    suite.addTest(TestAdminMgr('test08_add_object'))
    suite.addTest(TestAdminMgr('test09_add_perm'))
    suite.addTest(TestAdminMgr('test10_add_user'))
    suite.addTest(TestAdminMgr('test11_assign_user'))
    suite.addTest(TestAdminMgr('test12_grant'))
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())