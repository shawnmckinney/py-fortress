'''
@copyright: 2022 - Symas Corporation
'''

import unittest
import tempfile
import os
from rbac.model import User, Role
from rbac.util import Config
from rbac.dao_factory import get_userdao, get_roledao, get_dao_backend

class TestBackendSelection(unittest.TestCase):
    """
    Test the backend selection mechanism
    """

    def setUp(self):
        """Store original config"""
        self.original_backend = Config.getDefault('backend', 'ldap')
    
    def tearDown(self):
        """Restore original config"""
        Config.current['data']['backend'] = self.original_backend

    def test_backend_detection(self):
        """
        Test that the correct backend is detected from config
        """
        # Test SQL backend detection
        Config.current['data']['backend'] = 'sql'
        self.assertEqual(get_dao_backend(), 'sql')
        
        # Test file backend detection
        Config.current['data']['backend'] = 'file'
        self.assertEqual(get_dao_backend(), 'file')
        
        # Test LDAP backend detection (default)
        Config.current['data']['backend'] = 'ldap'
        self.assertEqual(get_dao_backend(), 'ldap')

    def test_dao_selection(self):
        """
        Test that the correct DAO modules are selected based on backend
        """
        # Test SQL DAO selection
        Config.current['data']['backend'] = 'sql'
        userdao = get_userdao()
        self.assertEqual(userdao.__name__, 'rbac.sql.userdao')
        
        roledao = get_roledao()
        self.assertEqual(roledao.__name__, 'rbac.sql.roledao')
        
        # Test file DAO selection
        Config.current['data']['backend'] = 'file'
        userdao = get_userdao()
        self.assertEqual(userdao.__name__, 'rbac.file.userdao')
        
        roledao = get_roledao()
        self.assertEqual(roledao.__name__, 'rbac.file.roledao')

    def test_admin_api_backend_switching(self):
        """
        Test that admin API works with different backends
        """
        import rbac.admin as admin
        
        # Test with SQL backend
        Config.current['data']['backend'] = 'sql'
        
        test_user_sql = User(
            uid='backendtest1',
            cn='Backend Test',
            sn='Test', 
            password='test123',
            description='Test user for backend switching'
        )
        
        try:
            # This should use SQL backend
            admin.add_user(test_user_sql)
            
            # Verify user was created in SQL backend
            userdao = get_userdao()
            read_user = userdao.read(User(uid='backendtest1'))
            self.assertEqual(read_user.uid, 'backendtest1')
            
            # Clean up
            admin.delete_user(User(uid='backendtest1'))
            
        except Exception as e:
            self.fail(f'SQL backend admin API test failed: {e}')

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestBackendSelection('test_backend_detection'))
    suite.addTest(TestBackendSelection('test_dao_selection'))
    suite.addTest(TestBackendSelection('test_admin_api_backend_switching'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())