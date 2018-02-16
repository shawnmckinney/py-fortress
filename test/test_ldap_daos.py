'''
Created on Feb 10, 2018

@author: smckinn
'''

import unittest
from ldap import userdao, permdao
from model import User, Permission
from util import Config
import logging

Config.load('py-fortress-cfg.json')
logging.basicConfig(filename='py-fortress-test.log', level=logging.INFO)


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

def print_constraint (constraint, label):
        print('\t' + label)    
        print('\t\t' + 'name=' + constraint.name)
        print('\t\t' + 'timeout=' + constraint.timeout)
        print('\t\t' + 'beginTime=' + constraint.beginTime)
        print('\t\t' + 'endTime=' + constraint.endTime)
        print('\t\t' + 'beginDate=' + constraint.beginDate)
        print('\t\t' + 'endDate=' + constraint.endDate)
        print('\t\t' + 'beginLockDate=' + constraint.beginLockDate)
        print('\t\t' + 'endLockDate=' + constraint.endLockDate)
        print('\t\t' + 'dayMask=' + constraint.dayMask)

def print_user (entity, label):
        print(label)
        print('\t' + 'uid=' + str(entity.uid))
        print('\t' + 'dn=' + str(entity.dn))
        print('\t' + 'cn=' + str(entity.cn))
        print('\t' + 'sn=' + str(entity.sn))
        print('\t' + 'description=' + str(entity.description))            
        print('\t' + 'ou=' + str(entity.ou))
        print('\t' + 'internalId=' + str(entity.internalId))
        print('\t' + 'roles=' + str(entity.roles))
        print('\t' + 'pwPolicy=' + str(entity.pwPolicy))                
        print('\t' + 'displayName=' + str(entity.displayName))        
        print('\t' + 'employeeType=' + str(entity.employeeType))
        print('\t' + 'title=' + str(entity.title))
        print('\t' + 'phones=' + str(entity.phones))
        print('\t' + 'mobiles=' + str(entity.mobiles))
        print('\t' + 'emails=' + str(entity.emails))        
        print('\t' + 'reset=' + str(entity.reset))
        print('\t' + 'lockedTime=' + str(entity.lockedTime))
        print('\t' + 'system=' + str(entity.system))
        print('\t' + 'props=' + str(entity.props))        
        print('\t' + 'departmentNumber=' + str(entity.departmentNumber))
        print('\t' + 'l=' + str(entity.l))
        print('\t' + 'physicalDeliveryOfficeName=' + str(entity.physicalDeliveryOfficeName))
        print('\t' + 'postalCode=' + str(entity.postalCode))
        print('\t' + 'roomNumber=' + str(entity.roomNumber))
        print_constraint (entity.constraint, "User Constraint:")
        for idx, constraint in enumerate(entity.roleConstraints) :
            print_constraint (constraint, "User-Role Constraint[" + str(idx+1) + "]:")
            
        print("*************** " + label + " *******************")

    
def print_perm (entity, label):
        print(label)
        print('\t' + 'objName=' + str(entity.objName))
        print('\t' + 'opName=' + str(entity.opName))
        print('\t' + 'objId=' + str(entity.objId))
        print('\t' + 'description=' + str(entity.description))            
        print('\t' + 'internalId=' + str(entity.internalId))        
        print('\t' + 'abstractName=' + str(entity.abstractName))
        print('\t' + 'type=' + str(entity.type))
        print('\t' + 'users=' + str(entity.users))
        print('\t' + 'roles=' + str(entity.roles))        
        print('\t' + 'dn=' + str(entity.dn))
        print('\t' + 'props=' + str(entity.props))
        
                
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
            #usr.uid = "jtsTU11User1"
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :            
                print_user(entity, "User[" + str(idx+1) + "]:")
        except Exception as e:
            self.fail('user search failed, exception=' + str(e))

            
    def test_search_perms(self):
        """
        Test the perm search by objName and opName in ldap
        """
        print('test search perms by objNm')        
        try:
            prm = Permission()
            prm.objName = "TOB*"
            prm.opName = "TOP*"            
            pList = permdao.search(prm)
            for idx, entity in enumerate(pList) :            
                print_perm(entity, "Perm[" + str(idx+1) + "]:")
        except Exception as e:
            self.fail('perm search failed, exception=' + str(e))

            
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDaos('test_search_users'))    
    suite.addTest(TestDaos('test_search_perms'))    
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
