'''
Created on Feb 10, 2018

@author: smckinn
'''

import unittest
import trace
import userdao
import user
from config import Config
import logging

Config.load('py-fortress-cfg.json')
logging.basicConfig(filename='py-fortress-test.log', level=logging.INFO)


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

     
def print_user (entity, label):
        print(label)
        print('uid=' + str(entity.uid))    
        print('ou=' + str(entity.ou))
        print("*************** " + label + " *******************")

    
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
            usr = user.User()
            usr.uid = "jts*"
            uList = userdao.search(usr)
            ctr = 1;
            for entity in uList:
                print_user(entity, "search entry " + str(ctr))
                ctr += 1
        except Exception as e:
            self.fail('user search failed, exception=' + str(e))

            
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDaos('test_search_users'))    
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
