'''
@copyright: 2022 - Symas Corporation
'''

import unittest
from rbac.ldap import ditdao
from rbac.util import global_ids
from rbac.cli.utils import print_ln


class BasicTestSuite(unittest.TestCase):
    """These tests the py-fortress DIT add and del functions."""
                

class TestDitDao(unittest.TestCase):
    """
    Test the DIT dao funcs
    """    
                     
                      
    def test01_del_containers(self):
        """
        Test the delete ou method
        """
        print_ln('test_del_containers')

        try:
            ditdao.delete_ou(global_ids.USER_OU)
            ditdao.delete_ou(global_ids.ROLE_OU)
            ditdao.delete_ou(global_ids.PERM_OU)
            print('test_del_containers success')
        except Exception as e:
            error = 'test_del_containers errpr=' + e.msg
            print(error)
            #self.fail(error)


    def test02_del_suffix(self):
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


    def test03_bootstrap(self):
        """
        Create the DIT based on the config
        """
        print_ln('test_bootstrap')
        try:
            ditdao.bootstrap()            
            print('test_bootstrap success')                                
        except Exception as e:
            error = 'test_bootstrap errpr=' + e.msg
            print(error)
            #self.fail(error)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDitDao('test01_del_containers'))
    suite.addTest(TestDitDao('test02_del_suffix'))
    suite.addTest(TestDitDao('test03_bootstrap'))
    return suite

 
def main():
    # My code here
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())


if __name__ == "__main__":
    main()
    