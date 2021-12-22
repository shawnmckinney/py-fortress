'''
@copyright: 2022 - Symas Corporation
'''

import unittest
from rbac.ldap import InvalidCredentials
from rbac import access, review
from rbac.model import User
from rbac.cli.utils import print_ln
import sys


class BasicTestSuite(unittest.TestCase):
    """These tests the py-fortress access functions."""
                

class TestAccessMgr(unittest.TestCase):
    """
    Test the access funcs
    """    

    def test01_create_sessions(self):
        """
        Test the create_session method
        """
        print_ln('test create sessions')
                                             
        try:
            usr = User(uid = "py-user*")    
            uList = review.find_users(usr)
            loop_cnt = len(uList)
            for idx, entity in enumerate(uList) :
                if idx % 10 == 0:
                    sys.stdout.write('')
                    sys.stdout.flush()
                entity.password = 'password'
                try:
                    session = access.create_session(entity, False)
                    if session is None:
                        self.fail('test create sessions failed ' + entity.uid)
                except InvalidCredentials as e:
                    print_ln(e.msg)                    
            print()
        except Exception as e:
            self.fail('user create_session exception=' + e.msg)


    def test02_user_roles(self):
        """
        Test the user_roles & is_user_in_role method
        """
        print_ln('test user_roles')        
        try:
            usr = User(uid = "py-user*")
            uList = review.find_users(usr)
            for idx, entity in enumerate(uList) :
                if idx % 10 == 0:
                    sys.stdout.write('')
                    sys.stdout.flush()           
                entity.password = 'password'     
                session = access.create_session(entity, False)
                if session is None:
                    self.fail('test_user_roles failed ' + entity.uid)
                    
                if session.user.roles is not None and len(session.user.roles) > 0:                    
                    roles = access.session_roles(session)
                    for role in roles:
                        result = access.is_user_in_role(session, role.name)
                        if not result:
                            self.fail('test_user_roles failed uid=' + entity.uid + ', role=' + role)
            print()                                                                            
        except Exception as e:
            self.fail('test_user_roles exception=' + e)


    def test03_active_roles(self):
        """
        Test the add_active_role & drop_active_role methods
        """
        print_ln('test active_roles')        
        try:
            usr = User(uid = "py-user*")
            uList = review.find_users(usr)
            for idx, entity in enumerate(uList) :
                if idx % 10 == 0:
                    sys.stdout.write('')
                    sys.stdout.flush()                    
                
                entity.password = 'password'
                session = access.create_session(entity, False)
                if session is None:
                    self.fail('test_active_roles failed ' + entity.uid)
                    
                if session.user.roles is not None and len(session.user.roles) > 0:                    
                    roles = access.session_roles(session)
                    active_roles = list(roles)
                    
                    # now deactivate all of the roles:
                    for idx2, role in enumerate(active_roles):
                        if idx2 % 10 == 0:
                            sys.stdout.write('`')
                            sys.stdout.flush()                            
                        
                        result = access.is_user_in_role(session, role.name)
                        if not result:
                            self.fail('test_active_roles failed uid=' + entity.uid + ', role=' + role)
                        access.drop_active_role(session, role.name)
                        result = access.is_user_in_role(session, role.name)
                        if result:
                            self.fail('test_active_roles negative failed uid=' + entity.uid + ', role=' + role)
                            
                    if session.user.roles is None or len(session.user.roles) > 0:                    
                        self.fail('test_active_roles did not inactivate all roles in session for uid=' + entity.uid)
                            
                    # now activate all of the roles once again:
                    for idx2, role in enumerate(active_roles):
                        if idx2 % 10 == 0:
                            sys.stdout.write('`')
                            sys.stdout.flush()
                            
                        result = access.is_user_in_role(session, role.name)
                        if result:
                            self.fail('test_active_roles failed inactive negative check uid=' + entity.uid + ', role=' + role)
                        access.add_active_role(session, role.name)
                        result = access.is_user_in_role(session, role.name)
                        if not result:
                            self.fail('test_active_roles failed inactive positive check uid=' + entity.uid + ', role=' + role)
                            
                    if session.user.roles is None or len(session.user.roles) != len(active_roles):                    
                        self.fail('test_active_roles did not activate all roles in session for uid=' + entity.uid)
                            
            print()                                                                            
        except Exception as e:
            self.fail('test_active_roles exception=' + e.msg)


    def test04_session_permissions(self):
        """
        Test the session_perms & check_access method
        """
        print_ln('test session_perms')        
        try:
            usr = User(uid = "py-user*")
            uList = review.find_users(usr)
            for idx, entity in enumerate(uList) :
                if idx % 10 == 0:
                    sys.stdout.write('')
                    sys.stdout.flush()

                entity.password = 'password'                                    
                session = access.create_session(entity, False)
                if session is None:
                    self.fail('test_session_permissions failed ' + entity.uid)
                if session.user.roles is not None and len(session.user.roles) > 0:                    
                    perms = access.session_perms(session)
                    for idx2, perm in enumerate(perms):
                        if idx2 % 10 == 0:
                            sys.stdout.write('`')
                            sys.stdout.flush()
                                                        
                        result = access.check_access(session, perm)
                        if not result:
                            self.fail('test_session_permissions failed uid=' + entity.uid + ', perm obj name=' + perm.obj_name + ', op name=' + perm.op_name + ', obj id=' + perm.obj_id)                                                
            print()
        except Exception as e:
            self.fail('test_session_permissions exception=' + e.msg)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAccessMgr('test01_create_sessions'))
    suite.addTest(TestAccessMgr('test02_user_roles'))
    suite.addTest(TestAccessMgr('test03_active_roles'))
    suite.addTest(TestAccessMgr('test04_session_permissions'))
       
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())