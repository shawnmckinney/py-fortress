'''
@copyright: 2022 - Symas Corporation
'''

import unittest
from rbac import review
from rbac.model import User, Role, Perm
from rbac.cli.utils import print_ln, print_entity


class BasicTestSuite(unittest.TestCase):
    """These tests the py-fortress review functions."""
                

class TestReivewMgr(unittest.TestCase):
    """
    Test the review funcs
    """    

    def test01_assigned_users(self):
        """
        Test the assigned users method
        """
        print_ln('test_assigned_users')
        
        try:
            rList = review.find_roles(Role(name='py-role*'))
            for rle in rList:                       
                print_ln("Assigned users role=" + rle.name)
                uList = review.assigned_users(rle)
                for user in uList:                       
                    print_ln("Assigned user=" + user, 1)
        except Exception as e:
            self.fail('test_assigned_users failed, exception=' + e.msg)


    def test02_assigned_roles(self):
        """
        Test the assigned roles method
        """
        print_ln('test_assigned_roles')
        
        try:
            uList = review.find_users(User(uid='py-user*'))
            for usr in uList:                       
                print_ln("Assigned roles user=" + usr.uid)
                rList = review.assigned_roles(usr)
                for role in rList:                       
                    print_entity(role, "Assigned role", 1)
        except Exception as e:
            self.fail('test_assigned_roles failed, exception=' + e.msg)


    def test03_perm_roles(self):
        """
        Test the perm roles method
        """
        print_ln('test16_perm_roles')
        
        try:
            pList = review.find_perms(Perm(obj_name='py-obj*', op_name='*'))
            for perm in pList:                       
                print_ln("Role Perm obj name=" + perm.obj_name + ', op=' + perm.op_name + ', id=' + perm.obj_id)
                rList = review.perm_roles(perm)
                for role in rList:
                    print_ln("Assigned role=" + role, 1)
        except Exception as e:
            self.fail('test16_perm_roles failed, exception=' + e.msg)


    def test04_role_perms(self):
        """
        Test the role perms method
        """
        print_ln('test_role_perms')
        
        try:
            rList = review.find_roles(Role(name='py-role*'))
            for rle in rList:                       
                print_ln("Perm Roles name=" + rle.name)
                pList = review.role_perms(rle)
                for perm in pList:
                    print_ln("Assigned perm obj name=" + perm.obj_name + ', op name=' + perm.op_name + ', obj id=' + perm.obj_id, 1)
        except Exception as e:
            self.fail('test_role_perms failed, exception=' + e.msg)


    def test05_user_perms(self):
        """
        Test the user perms method
        """
        print_ln('test_user_perms')
        
        try:
            uList = review.find_users(User(uid='py-user*'))
            for usr in uList:                       
                print_ln("Assigned perms user=" + usr.uid)
                pList = review.user_perms(usr)
                for perm in pList:                       
                    print_ln("Assigned perm obj name=" + perm.obj_name + ', op name=' + perm.op_name + ', obj id=' + perm.obj_id, 1)                    
        except Exception as e:
            self.fail('test_user_perms failed, exception=' + e.msg)


    def test06_perm_users(self):
        """
        Test the perm users method
        """
        print_ln('test_perm_users')
        
        try:
            pList = review.find_perms(Perm(obj_name='py-obj*', op_name='*'))
            for perm in pList:                       
                print_ln("Perm obj name=" + perm.obj_name + ', op=' + perm.op_name + ', id=' + perm.obj_id)
                uList = review.perm_users(perm)
                for user in uList:
                    print_ln("Assigned user=" + user.uid, 1)
        except Exception as e:
            self.fail('test_perm_users failed, exception=' + e.msg)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestReivewMgr('test01_assigned_users'))
    suite.addTest(TestReivewMgr('test02_assigned_roles'))
    suite.addTest(TestReivewMgr('test03_perm_roles'))
    suite.addTest(TestReivewMgr('test04_role_perms'))
    suite.addTest(TestReivewMgr('test05_user_perms'))
    suite.addTest(TestReivewMgr('test06_perm_users'))
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())