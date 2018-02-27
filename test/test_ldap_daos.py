'''
Created on Feb 10, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

import unittest
from ldap import userdao, permdao, LdapException, InvalidCredentials
from model import User, Permission
from test.utils import print_user, print_perm, print_constraint


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""
                
class TestDaos(unittest.TestCase):
    """
    Test the user functions from the userdaomodule
    """    
    
    def test_search_users(self):
        """
        Test the user search by uid in ldap
        """
        print('test search users by uid')        
        try:
            usr = User(uid = "jtsUser1")
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :            
                print_user(entity, "User[" + str(idx+1) + "]:")
        except Exception as e:
            self.fail('user search failed, exception=' + str(e))

            
    def test_search_perms(self):
        """
        Test the perm search by obj_name and op_name in ldap
        """
        print('test search perms by objNm')        
        try:
            prm = Permission(obj_name = "TOB*", op_name = "TOP*")
            pList = permdao.search(prm)
            for idx, entity in enumerate(pList) :            
                print_perm(entity, "Perm[" + str(idx+1) + "]:")
        except Exception as e:
            self.fail('perm search failed, exception=' + str(e))

            
    def test_bind_users(self):
        """
        Test the user bind
        """
        print('test bind users')        
        try:
            usr = User(uid = "jtsuser*")
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :
                entity.password = 'passw0rd' + str(idx+1)      
                result = userdao.authenticate(entity)
                if result is False:
                    self.fail('test bind failed ' + entity.uid)
                          
        except InvalidCredentials:
            self.fail('user bind invalid creds, user=' + entity.uid)
        except Exception as e:
            self.fail('user bind exception=' + str(e))

    def test_bind_users_negative(self):
        """
        Test the user bind
        """
        print('test bind users')        
        try:
            usr = User(uid = "jtsuser*")
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :
                entity.password = 'notrightpassword'
                try:      
                    userdao.authenticate(entity)
                    self.fail('test bind negative failed ' + entity.uid)
                except InvalidCredentials:
                    pass
                         
        except Exception as e:
            self.fail('user bind failed, exception=' + str(e))

            
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDaos('test_search_users'))
    suite.addTest(TestDaos('test_bind_users'))
    suite.addTest(TestDaos('test_bind_users_negative'))               
    suite.addTest(TestDaos('test_search_perms'))    
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
