'''
Created on Mar 2, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

import unittest
from pyfortress.ldap import InvalidCredentials
from pyfortress.impl import access_mgr, review_mgr
from pyfortress.model import User
from pyfortress.test import print_ln
import sys


class BasicTestSuite(unittest.TestCase):
    """These tests the py-fortress access_mgr functions."""
                

class TestAccessMgr(unittest.TestCase):
    """
    Test the access_mgr funcs
    """    

    def test_create_sessions(self):
        """
        Test the create_session method
        """
        print_ln('test create sessions')
                                             
        try:
            usr = User(uid = "py-user*")    
            uList = review_mgr.find_users(usr)            
            loop_cnt = len(uList)
            for idx, entity in enumerate(uList) :
                if idx % 10 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                entity.password = 'password'
                try:
                    session = access_mgr.create_session(entity, False)
                    if session is None:
                        self.fail('test create sessions failed ' + entity.uid)
                except InvalidCredentials as e:
                    print_ln(e.msg)                    
            print()
        except Exception as e:
            self.fail('user create_session exception=' + e.msg)


    def test_user_roles(self):
        """
        Test the user_roles & is_user_in_role method
        """
        print_ln('test user_roles')        
        try:
            usr = User(uid = "py-user*")
            uList = review_mgr.find_users(usr)                        
            for idx, entity in enumerate(uList) :
                if idx % 10 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()           
                entity.password = 'password'     
                session = access_mgr.create_session(entity, False)
                if session is None:
                    self.fail('test_user_roles failed ' + entity.uid)
                    
                if session.user.roles is not None and len(session.user.roles) > 0:                    
                    roles = access_mgr.session_roles(session)
                    for role in roles:
                        result = access_mgr.is_user_in_role(session, role.name)
                        if not result:
                            self.fail('test_user_roles failed uid=' + entity.uid + ', role=' + role)
            print()                                                                            
        except Exception as e:
            self.fail('test_user_roles exception=' + e.msg)


    def test_active_roles(self):
        """
        Test the add_active_role & drop_active_role methods
        """
        print_ln('test active_roles')        
        try:
            usr = User(uid = "py-user*")
            uList = review_mgr.find_users(usr)                        
            for idx, entity in enumerate(uList) :
                if idx % 10 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()                    
                
                entity.password = 'password'
                session = access_mgr.create_session(entity, False)
                if session is None:
                    self.fail('test_active_roles failed ' + entity.uid)
                    
                if session.user.roles is not None and len(session.user.roles) > 0:                    
                    roles = access_mgr.session_roles(session)
                    active_roles = list(roles)
                    
                    # now deactivate all of the roles:
                    for idx2, role in enumerate(active_roles):
                        if idx2 % 10 == 0:
                            sys.stdout.write('`')
                            sys.stdout.flush()                            
                        
                        result = access_mgr.is_user_in_role(session, role.name)
                        if not result:
                            self.fail('test_active_roles failed uid=' + entity.uid + ', role=' + role)
                        access_mgr.drop_active_role(session, role.name)
                        result = access_mgr.is_user_in_role(session, role.name)
                        if result:
                            self.fail('test_active_roles negative failed uid=' + entity.uid + ', role=' + role)
                            
                    if session.user.roles is None or len(session.user.roles) > 0:                    
                        self.fail('test_active_roles did not inactivate all roles in session for uid=' + entity.uid)
                            
                    # now activate all of the roles once again:
                    for idx2, role in enumerate(active_roles):
                        if idx2 % 10 == 0:
                            sys.stdout.write('`')
                            sys.stdout.flush()
                            
                        result = access_mgr.is_user_in_role(session, role.name)
                        if result:
                            self.fail('test_active_roles failed inactive negative check uid=' + entity.uid + ', role=' + role)
                        access_mgr.add_active_role(session, role.name)
                        result = access_mgr.is_user_in_role(session, role.name)
                        if not result:
                            self.fail('test_active_roles failed inactive positive check uid=' + entity.uid + ', role=' + role)
                            
                    if session.user.roles is None or len(session.user.roles) != len(active_roles):                    
                        self.fail('test_active_roles did not activate all roles in session for uid=' + entity.uid)
                            
            print()                                                                            
        except Exception as e:
            self.fail('test_active_roles exception=' + e.msg)


    def test_session_permissions(self):
        """
        Test the session_perms & check_access method
        """
        print_ln('test session_perms')        
        try:
            usr = User(uid = "py-user*")
            uList = review_mgr.find_users(usr)                        
            for idx, entity in enumerate(uList) :
                if idx % 10 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()

                entity.password = 'password'                                    
                session = access_mgr.create_session(entity, False)
                if session is None:
                    self.fail('test_session_permissions failed ' + entity.uid)
                if session.user.roles is not None and len(session.user.roles) > 0:                    
                    perms = access_mgr.session_perms(session)
                    for idx2, perm in enumerate(perms):
                        if idx2 % 10 == 0:
                            sys.stdout.write('`')
                            sys.stdout.flush()
                                                        
                        result = access_mgr.check_access(session, perm)
                        if not result:
                            self.fail('test_session_permissions failed uid=' + entity.uid + ', perm obj name=' + perm.obj_name + ', op name=' + perm.op_name + ', obj id=' + perm.obj_id)                                                
            print()
        except Exception as e:
            self.fail('test_session_permissions exception=' + e.msg)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAccessMgr('test_create_sessions'))
    suite.addTest(TestAccessMgr('test_user_roles'))
    suite.addTest(TestAccessMgr('test_active_roles'))         
    suite.addTest(TestAccessMgr('test_session_permissions'))
       
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())