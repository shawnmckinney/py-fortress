'''
@copyright: 2022 - Symas Corporation
'''

import unittest
from rbac.model import User, Role, Perm, PermObj
from rbac.cli.utils import print_ln, print_entity
from rbac.sql import userdao, roledao, permdao

class TestSqlDaos(unittest.TestCase):
    """
    Test the SQL backend DAO modules
    """

    def test_user_operations(self):
        """
        Test user CRUD operations in SQL backend
        """
        print_ln('test SQL user operations')
        
        # Test user creation
        test_user = User(
            uid='sqltest1',
            cn='SQL Test User',
            sn='User',
            password='testpass123',
            description='Test user for SQL backend',
            emails=['test@example.com'],
            phones=['555-1234']
        )
        
        try:
            # Create user
            created_user = userdao.create(test_user)
            self.assertEqual(created_user.uid, 'sqltest1')
            self.assertEqual(created_user.cn, 'SQL Test User')
            
            # Read user
            read_user = userdao.read(User(uid='sqltest1'))
            self.assertEqual(read_user.uid, 'sqltest1')
            self.assertEqual(read_user.description, 'Test user for SQL backend')
            
            # Search users
            search_results = userdao.search(User(uid='sqltest*'))
            self.assertGreaterEqual(len(search_results), 1)
            
            # Authenticate user
            auth_result = userdao.authenticate(User(uid='sqltest1', password='testpass123'))
            self.assertTrue(auth_result)
            
            # Update user (only description)
            update_user = User(uid='sqltest1', description='Updated description')
            userdao.update(update_user)
            
            # Verify update
            updated_user = userdao.read(User(uid='sqltest1'))
            self.assertEqual(updated_user.description, 'Updated description')
            
            # Delete user
            userdao.delete(User(uid='sqltest1'))
            
            # Verify deletion
            with self.assertRaises(Exception):
                userdao.read(User(uid='sqltest1'))
                
        except Exception as e:
            self.fail('User operations failed, exception=' + str(e))

    def test_role_operations(self):
        """
        Test role CRUD operations in SQL backend
        """
        print_ln('test SQL role operations')
        
        test_role = Role(
            name='sqlrole1',
            description='Test role for SQL backend',
            props=['test:value']
        )
        
        try:
            # Create role
            created_role = roledao.create(test_role)
            self.assertEqual(created_role.name, 'sqlrole1')
            
            # Read role
            read_role = roledao.read(Role(name='sqlrole1'))
            self.assertEqual(read_role.name, 'sqlrole1')
            self.assertEqual(read_role.description, 'Test role for SQL backend')
            
            # Search roles
            search_results = roledao.search(Role(name='sqlrole*'))
            self.assertGreaterEqual(len(search_results), 1)
            
            # Update role
            update_role = Role(name='sqlrole1', description='Updated role description')
            roledao.update(update_role)
            
            # Verify update
            updated_role = roledao.read(Role(name='sqlrole1'))
            self.assertEqual(updated_role.description, 'Updated role description')
            
            # Delete role
            roledao.delete(Role(name='sqlrole1'))
            
            # Verify deletion
            with self.assertRaises(Exception):
                roledao.read(Role(name='sqlrole1'))
                
        except Exception as e:
            self.fail('Role operations failed, exception=' + str(e))

    def test_permission_operations(self):
        """
        Test permission and permission object CRUD operations
        """
        print_ln('test SQL permission operations')
        
        test_obj = PermObj(
            obj_name='sqltestobj1',
            description='Test object for SQL backend'
        )
        
        test_perm = Perm(
            obj_name='sqltestobj1',
            op_name='execute',
            description='Test permission for SQL backend'
        )
        
        try:
            # Create permission object
            created_obj = permdao.create_obj(test_obj)
            self.assertEqual(created_obj.obj_name, 'sqltestobj1')
            
            # Create permission
            created_perm = permdao.create(test_perm)
            self.assertEqual(created_perm.obj_name, 'sqltestobj1')
            self.assertEqual(created_perm.op_name, 'execute')
            
            # Read permission
            read_perm = permdao.read(Perm(obj_name='sqltestobj1', op_name='execute'))
            self.assertEqual(read_perm.description, 'Test permission for SQL backend')
            
            # Search permissions
            search_results = permdao.search(Perm(obj_name='sqltestobj*'))
            self.assertGreaterEqual(len(search_results), 1)
            
            # Clean up
            permdao.delete(Perm(obj_name='sqltestobj1', op_name='execute'))
            permdao.delete_obj(PermObj(obj_name='sqltestobj1'))
            
        except Exception as e:
            self.fail('Permission operations failed, exception=' + str(e))

    def test_role_membership(self):
        """
        Test role membership operations
        """
        print_ln('test SQL role membership')
        
        test_role = Role(name='membershiprole1', description='Test membership role')
        
        try:
            # Create role
            roledao.create(test_role)
            
            # Add member
            roledao.add_member(test_role, 'testuser1')
            
            # Get members
            members = roledao.get_members(test_role)
            self.assertIn('testuser1', members)
            
            # Remove member
            roledao.remove_member(test_role, 'testuser1')
            
            # Verify removal
            members = roledao.get_members(test_role)
            self.assertNotIn('testuser1', members)
            
            # Clean up
            roledao.delete(test_role)
            
        except Exception as e:
            self.fail('Role membership operations failed, exception=' + str(e))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestSqlDaos('test_user_operations'))
    suite.addTest(TestSqlDaos('test_role_operations'))
    suite.addTest(TestSqlDaos('test_permission_operations'))
    suite.addTest(TestSqlDaos('test_role_membership'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())