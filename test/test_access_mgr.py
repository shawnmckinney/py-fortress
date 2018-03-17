'''
Created on Mar 2, 2018

@author: smckinn
'''

import unittest
from ldap import userdao, InvalidCredentials
from impl import access_mgr
from model import User
from test.utils import print_ln


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
            #usr = User(uid = "jtsuser*")
            usr = User(uid = "jts*")
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :
                #print_entity(entity, 'test_create_sessions index=' + str(idx) + ', uid=' + entity.uid)
                entity.password = 'passw0rd' + str(idx+1)
                try:
                    session = access_mgr.create_session(entity, True)
                    if session is None:
                        self.fail('test create sessions failed ' + entity.uid)
                except InvalidCredentials as e:
                    print_ln(str(e))
                    
        except Exception as e:
            self.fail('user create_session exception=' + str(e))


    def test_user_roles(self):
        """
        Test the user_roles & is_user_in_role method
        """
        print_ln('test user_roles')        
        try:
            usr = User(uid = "jts*")
            #usr = User(uid = "jtsuser1")
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :
                #print_entity(entity, 'test_is_user_in_role index=' + str(idx) + ', uid=' + entity.uid)
                session = access_mgr.create_session(entity, True)
                if session is None:
                    self.fail('test_user_roles failed ' + entity.uid)
                    
                if session.user.roles is not None and len(session.user.roles) > 0:                    
                    roles = access_mgr.session_roles(session)
                    for role in roles:
                        result = access_mgr.is_user_in_role(session, role.name)
                        if not result:
                            self.fail('test_user_roles failed uid=' + entity.uid + ', role=' + role)                                                
        except Exception as e:
            self.fail('test_user_roles exception=' + str(e))


    def test_session_permissions(self):
        """
        Test the session_permissions & check_access method
        """
        print_ln('test session_permissions')        
        try:
            usr = User(uid = "jts*")
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :
                #print_entity(entity, 'test_is_user_in_role index=' + str(idx) + ', uid=' + entity.uid)
                session = access_mgr.create_session(entity, True)
                if session is None:
                    self.fail('test_session_permissions failed ' + entity.uid)
                if session.user.roles is not None and len(session.user.roles) > 0:                    
                    perms = access_mgr.session_permissions(session)
                    for perm in perms:
                        result = access_mgr.check_access(session, perm)
                        if not result:
                            self.fail('test_session_permissions failed uid=' + entity.uid + ', perm obj name=' + perm.obj_name + ', op name=' + perm.op_name + ', obj id=' + perm.obj_id)                                                
        except Exception as e:
            self.fail('test_session_permissions exception=' + str(e))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAccessMgr('test_create_sessions'))
    suite.addTest(TestAccessMgr('test_user_roles'))    
    suite.addTest(TestAccessMgr('test_session_permissions'))    
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())