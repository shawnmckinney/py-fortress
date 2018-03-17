'''
Created on Feb 10, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

import unittest
from ldap import userdao, permdao, roledao, InvalidCredentials
from model import User, Permission, Role
from test.utils import print_user, print_role, print_ln, print_entity


class BasicTestSuite(unittest.TestCase):
    """These tests assume fortress user and permission data has been pre-loaded into Ldap, i.e. via apache fortress administrative functions."""
                
class TestDaos(unittest.TestCase):
    """
    Test the user functions from the user and perm dao modules
    """    
    
    def test_search_users(self):
        """
        Test the user search by uid in ldap
        """
        print_ln('test search users by uid')        
        try:
            usr = User(uid = "jts*")
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :            
                print_user(entity, "User[" + str(idx+1) + "]:")
        except Exception as e:
            self.fail('user search failed, exception=' + str(e))

            
    def test_search_perms(self):
        """
        Test the perm search by obj_name and op_name in ldap
        """
        print_ln('test search perms by objNm')        
        try:
            prm = Permission(obj_name = "TOB*", op_name = "TOP*")
            pList = permdao.search(prm)
            for idx, entity in enumerate(pList) :            
                print_entity (entity, "Perm[" + str(idx+1) + "]:", 1)
        except Exception as e:
            self.fail('perm search failed, exception=' + str(e))

            
    def test_bind_users(self):
        """
        Test the user bind
        """
        print_ln('test bind users')        
        try:
            usr = User(uid = "jtsuser*")
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :
                entity.password = 'passw0rd' + str(idx+1)
                
                try:      
                    userdao.authenticate(entity)
                except InvalidCredentials as e:
                    print_ln(str(e))
                    #self.fail('user bind invalid creds, user=' + entity.uid)
                          
        except Exception as e:
            self.fail('user bind exception=' + str(e))


    def test_bind_users_negative(self):
        """
        Test the user bind
        """
        print_ln('test bind users')        
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


    def test_search_roles(self):
        """
        Test the role search by name in ldap
        """
        print_ln('test search roles by name')        
        try:
            rle = Role(name = "oam*")
            rList = roledao.search(rle)
            for idx, entity in enumerate(rList) :            
                print_role(entity, "Role[" + str(idx+1) + "]:")
        except Exception as e:
            self.fail('role search failed, exception=' + str(e))

                        
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDaos('test_search_users'))
    suite.addTest(TestDaos('test_bind_users'))
    suite.addTest(TestDaos('test_bind_users_negative'))               
    suite.addTest(TestDaos('test_search_perms'))   
    suite.addTest(TestDaos('test_search_roles'))     
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())