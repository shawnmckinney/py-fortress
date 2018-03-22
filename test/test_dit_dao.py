'''
Created on Mar 22, 2018

@author: smckinn
'''
'''
Created on Mar 18, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

import unittest
from ldap import ditdao
from test.utils import print_ln


class BasicTestSuite(unittest.TestCase):
    """These tests the py-fortress DIT add and del functions."""
                

class TestDitDao(unittest.TestCase):
    """
    Test the DIT dao funcs
    """    
                     
                      
    def test_add_containers(self):
        """
        Test the add suffix method
        """
        print_ln('test_add_containers')
        
        try:
            ditdao.create_ou('People')
            ditdao.create_ou('Roles')
            ditdao.create_ou('Perms')            
            print('test_add_containers success')                                
        except Exception as e:
            error = 'test_add_containers errpr=' + e.msg
            print(error)
            self.fail(error)


    def test_del_containers(self):
        """
        Test the delete ou method
        """
        print_ln('test_del_containers')
        
        try:
            ditdao.delete_ou('People')
            ditdao.delete_ou('Roles')
            ditdao.delete_ou('Perms')            
            print('test_del_containers success')                                
        except Exception as e:
            error = 'test_del_containers errpr=' + e.msg
            print(error)
            #self.fail(error)


    def test_add_suffix(self):
        """
        Test the add suffix method
        """
        print_ln('test_add_suffix')
        
        try:
            ditdao.create_suffix('example')            
            print('test_add_suffix success')                                
        except Exception as e:
            error = 'test_add_suffix errpr=' + e.msg
            print(error)
            #self.fail(error)


    def test_del_suffix(self):
        """
        Test the del suffix method
        """
        print_ln('test_del_suffix')
        
        try:
            ditdao.delete_suffix()            
            print('test_del_suffix success')                                
        except Exception as e:
            error = 'test_del_suffix errpr=' + e.msg
            print(error)
            #self.fail(error)


def suite():
    suite = unittest.TestSuite()
    
    # Teardown:
    suite.addTest(TestDitDao('test_del_containers'))
    suite.addTest(TestDitDao('test_del_suffix'))
    suite.addTest(TestDitDao('test_add_suffix'))
    suite.addTest(TestDitDao('test_add_containers'))              
      
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())