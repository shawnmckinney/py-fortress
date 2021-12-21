'''
@copyright: 2022 - Symas Corporation
'''

import unittest
from rbac.ldap import userdao, permdao, roledao, InvalidCredentials
from rbac.model import User, Perm, Role, PermObj
from rbac.tests import user_test_data, role_test_data
from rbac.cli.utils import print_user, print_role, print_ln, print_entity
from rbac.tests import perm_test_data


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
            self.fail('user search failed, exception=' + e.msg)

            
    def test_search_perms(self):
        """
        Test the perm search by obj_name and op_name in ldap
        """
        print_ln('test search perms by objNm')        
        try:
            prm = Perm(obj_name = "TOB*", op_name = "TOP*")
            pList = permdao.search(prm)
            for idx, entity in enumerate(pList) :            
                print_entity (entity, "Perm[" + str(idx+1) + "]:", 1)
        except Exception as e:
            self.fail('perm search failed, exception=' + e.msg)

            
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
                    print_ln(e.msg)
                    #self.fail('user bind invalid creds, user=' + entity.uid)
                          
        except Exception as e:
            self.fail('user bind exception=' + e.msg)


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
            self.fail('user bind failed, exception=' + e.msg)


    def test_search_roles(self):
        """
        Test the role search by name in ldap
        """
        print_ln('test search roles by name')        
        try:
            rle = Role(name = 'oam*')
            rList = roledao.search(rle)
            for idx, entity in enumerate(rList) :            
                print_role(entity, "Role[" + str(idx+1) + "]:")
        except Exception as e:
            self.fail('role search failed, exception=' + e.msg)

                        
    def test_create_roles(self):
        """
        Test the role create
        """
        print_ln('test create roles')
        rls = role_test_data.get_test_roles('py-test', 10)
        for rle in rls:
            try:                        
                rle = roledao.create(rle)
                print_role(rle, "Role Create")
            except Exception as e:
                self.fail('role create failed, exception=' + e.msg)


    def test_update_roles(self):
        """
        Test the role update
        """
        print_ln('test update roles')
        rls = role_test_data.get_test_roles('py-test', 10)
        for rle in rls:
            rle.description += '-updated'
            try:                        
                rle = roledao.update(rle)
                print_role(rle, "Role Update")
            except Exception as e:
                self.fail('role update failed, exception=' + e.msg)


    def test_delete_roles(self):
        """
        Test the role delete
        """
        print_ln('test delete roles')
        
        try:
            rList = roledao.search(Role(name='py-test*'))
            for rle in rList:                       
                rle = roledao.delete(rle)
                print_ln("Role Delete role=" + rle.name)
        except Exception as e:
            self.fail('role delete failed, exception=' + e.msg)


    def test_create_users(self):
        """
        Test the user create
        """
        print_ln('test create users')
        usrs = user_test_data.get_test_users('py-test', 10)
        for usr in usrs:
            try:                        
                entity = userdao.create(usr)
                print_user(entity, "User Create")
            except Exception as e:
                self.fail('user create failed, exception=' + e.msg)


    def test_update_users(self):
        """
        Test the user update
        """
        print_ln('test update users')
        usrs = user_test_data.get_test_users('py-test', 10)
        for usr in usrs:
            usr.description += '-updated'
            usr.cn += '-updated'
            usr.sn += '-updated'                        
            try:                        
                entity = userdao.update(usr)
                print_user(entity, "User Update")
            except Exception as e:
                self.fail('user update failed, exception=' + e.msg)


    def test_delete_users(self):
        """
        Test the user delete
        """
        print_ln('test delete users')
        
        try:
            uList = userdao.search(User(uid='py-test*'))
            for usr in uList:                       
                entity = userdao.delete(usr)
                print_ln("Delete user=" + entity.uid)
        except Exception as e:
            self.fail('user delete failed, exception=' + e.msg)


    def test_create_objects(self):
        """
        Test the object create
        """
        print_ln('test create objects')
        objs = perm_test_data.get_test_objs('py-test', 10)
        for obj in objs:
            try:                        
                entity = permdao.create_obj(obj)
                print_ln("Create object=" + entity.obj_name)                
            except Exception as e:
                self.fail('perm object create failed, exception=' + e.msg)


    def test_update_objects(self):
        """
        Test the object update
        """
        print_ln('test update objects')
        objs = perm_test_data.get_test_objs('py-test', 10)
        for obj in objs:
            obj.description += '-updated'
            obj.type += '-updated'                        
            try:                        
                entity = permdao.update_obj(obj)
                print_ln("Update object=" + entity.obj_name)                
            except Exception as e:
                self.fail('object update failed, exception=' + e.msg)


    def test_delete_objects(self):
        """
        Test the object delete
        """
        print_ln('test delete objects')
        
        try:
            oList = permdao.search_objs(PermObj(obj_name='py-test*'))
            for obj in oList:                       
                entity = permdao.delete_obj(obj)
                print_ln("Delete object=" + obj.obj_name)
        except Exception as e:
            self.fail('perm obj delete failed, exception=' + e.msg)


    def test_create_perms(self):
        """
        Test the perm create
        """
        print_ln('test create perms')
        perms = perm_test_data.get_test_perms('py-test', 10)
        for perm in perms:
            try:                        
                entity = permdao.create(perm)
                print_ln("Create perm obj=" + entity.obj_name + ', op=' + entity.op_name + ', id=' + entity.obj_id)                
            except Exception as e:
                self.fail('perm create failed, exception=' + e.msg)


    def test_update_perms(self):
        """
        Test the perm update
        """
        print_ln('test update perms')
        perms = perm_test_data.get_test_perms('py-test', 10)
        for perm in perms:
            perm.description += '-updated'
            perm.type += '-updated'                        
            try:                        
                entity = permdao.update(perm)
                print_ln("Update perm obj=" + entity.obj_name + ', op=' + entity.op_name + ', id=' + entity.obj_id)                
            except Exception as e:
                self.fail('perm update failed, exception=' + e.msg)


    def test_delete_perms(self):
        """
        Test the perm delete
        """
        print_ln('test delete perms')
        
        try:
            pList = permdao.search(Perm(obj_name='py-test*', op_name='*'))
            for perm in pList:                       
                entity = permdao.delete(perm)
                print_ln("Delete perm obj=" + perm.obj_name + ', op=' + perm.op_name + ', id=' + perm.obj_id)
        except Exception as e:
            self.fail('perm delete failed, exception=' + e.msg)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDaos('test_search_users'))
    suite.addTest(TestDaos('test_bind_users'))
    suite.addTest(TestDaos('test_bind_users_negative'))               
    suite.addTest(TestDaos('test_search_perms'))   
    suite.addTest(TestDaos('test_search_roles'))
    suite.addTest(TestDaos('test_delete_roles'))    
    suite.addTest(TestDaos('test_create_roles'))
    suite.addTest(TestDaos('test_update_roles'))
    suite.addTest(TestDaos('test_delete_users'))
    suite.addTest(TestDaos('test_create_users'))
    suite.addTest(TestDaos('test_update_users'))
    suite.addTest(TestDaos('test_delete_perms'))    
    suite.addTest(TestDaos('test_delete_objects'))
    suite.addTest(TestDaos('test_create_objects'))             
    suite.addTest(TestDaos('test_update_objects'))
    suite.addTest(TestDaos('test_create_perms'))
    suite.addTest(TestDaos('test_update_perms'))            
    return suite  

 
if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())