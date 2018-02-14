'''
Created on Feb 10, 2018

@author: smckinn
'''

import unittest
import trace
from ldap import userdao
from model import User
from util import Config
import logging

Config.load('py-fortress-cfg.json')
logging.basicConfig(filename='py-fortress-test.log', level=logging.INFO)


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

     
def print_user (entity, label):
        print(label)
        print('uid=' + str(entity.uid))
        print('dn=' + str(entity.dn))
        print('cn=' + str(entity.cn))
        print('sn=' + str(entity.sn))
        print('description=' + str(entity.description))            
        print('ou=' + str(entity.ou))
        print('internalId=' + str(entity.internalId))
        print('roles=' + str(entity.roles))
        print('pwPolicy=' + str(entity.pwPolicy))                
        print('displayName=' + str(entity.displayName))        
        print('employeeType=' + str(entity.employeeType))
        print('title=' + str(entity.title))
        print('phones=' + str(entity.phones))
        print('mobiles=' + str(entity.mobiles))
        print('emails=' + str(entity.emails))        
        print('reset=' + str(entity.reset))
        print('lockedTime=' + str(entity.lockedTime))
        print('system=' + str(entity.system))
        print('props=' + str(entity.props))        
        print('departmentNumber=' + str(entity.departmentNumber))
        print('l=' + str(entity.l))
        print('physicalDeliveryOfficeName=' + str(entity.physicalDeliveryOfficeName))
        print('postalCode=' + str(entity.postalCode))
        print('roomNumber=' + str(entity.roomNumber))
        
#         print('x=' + str(entity.x))
#         print('x=' + str(entity.x))
#         print('x=' + str(entity.x))
#         print('x=' + str(entity.x))
#         print('x=' + str(entity.x))
#         print('x=' + str(entity.x))
        
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
            usr = User()
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
