import unittest
from pyfortress.file import userdao,roledao,permdao,fileex,access_mgr
from pyfortress.model import User
from pyfortress.test import print_ln,print_entity

class TestAccessMgr(unittest.TestCase):
    """
    Test the access_mgr funcs
    """

    def test_create_sessions(self):
        """
        Test the create_session method
        """
        print_ln('test create sessions')

        try:
            for user in userdao.search(User(uid="*")):
                user.password = user.uid
                session = access_mgr.create_session(user, False)
                if session is None:
                    self.fail('create session {} returned None'.format(user.uid))
                print ('session made for user {}'.format(user.uid))
        except Exception as e:
            self.fail('user create_session exception=' + e.msg)

    def test_user_roles(self):
        """
        Test the user_roles & is_user_in_role method
        """
        print_ln('test user_roles')
        try:
            for user in userdao.search(User(uid="*")):
                user.password = user.uid
                session = access_mgr.create_session(user, False)
                if session is None:
                    self.fail('create session {} returned None'.format(user.uid))
                print ('session made for user {}'.format(user.uid))

                if session.user.roles is not None and len(session.user.roles) > 0:
                    roles = access_mgr.session_roles(session)
                    for role in roles:
                        result = access_mgr.is_user_in_role(session, role)
                        if not result:
                            self.fail('test_user_roles failed uid=' + entity.uid + ', role=' + role)
            print()
        except Exception as e:
            self.fail('test_user_roles exception=' + e.msg)


    def test_active_roles(self):
        """
        Test the add_active_role & drop_active_role methods
        """
        print_ln('test active_roles')
        try:
            u = userdao.read(User(uid="foouser1"))
            u.password="foouser1"
            session=access_mgr.create_session (u, False)

            if session.user.roles is not None and len(session.user.roles) > 0:
                for role in list(access_mgr.session_roles(session)):
                    access_mgr.drop_active_role(session, role)

                if session.user.roles is None or len(session.user.roles) > 0:
                    self.fail('test_active_roles did not inactivate all roles in session for uid=' + entity.uid)

                for role in list(u.roles):
                    access_mgr.add_active_role(session, role)

                if session.user.roles is None or len(session.user.roles) != len(u.roles):
                    self.fail('test_active_roles did not activate all roles in session for uid=' + entity.uid)

        except Exception as e:
            self.fail('test_active_roles exception=' + e.msg)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAccessMgr('test_create_sessions'))
    suite.addTest(TestAccessMgr('test_user_roles'))
    suite.addTest(TestAccessMgr('test_active_roles'))
#    suite.addTest(TestAccessMgr('test_session_permissions'))

    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
