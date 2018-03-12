'''
Created on Mar 2, 2018

@author: smckinn
'''

import unittest
from ldap import userdao, InvalidCredentials
from impl import access_mgr
from model import User, Permission
from test.utils import print_user, print_perm, print_ln


class BasicTestSuite(unittest.TestCase):
    """These tests the py-fortress access_mgr functions."""
                
class TestAccessMgr(unittest.TestCase):
    """
    Test the access_mgr funcs
    """    
    
    def test_create_session(self):
        """
        Test the user search by uid in ldap
        """
        print_ln('test search users by uid')        
        try:
            usr = User(uid = "jtsuser1")
            usr.password = 'passw0rd1'
            session = access_mgr.create_session(usr, False)
            print_user(usr, "CreateSession")
        except Exception as e:
            self.fail('test_create_session failed, exception=' + str(e))

                        
    def test_create_sessions(self):
        """
        Test the create_session method
        """
        print_ln('test create sessions')        
        try:
            usr = User(uid = "jtsuser*")
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :
                entity.password = 'passw0rd' + str(idx+1)
                session = access_mgr.create_session(entity, False)
                if session is None:
                    self.fail('test create sessions failed ' + entity.uid)
                          
        except InvalidCredentials:
            self.fail('user bind invalid creds, user=' + entity.uid)
        except Exception as e:
            self.fail('user bind exception=' + str(e))




            
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAccessMgr('test_create_sessions'))
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())