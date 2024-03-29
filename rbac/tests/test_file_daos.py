'''
@copyright: 2022 - Symas Corporation
'''
import unittest
from rbac.model import User,Perm
from rbac.cli.utils import print_ln, print_entity
from json import dumps

from rbac.file import userdao,permdao,fileex

class TestDaos(unittest.TestCase):
    """
    Test the user functions from the user and perm dao modules
    """

    def test_search_users(self):
        """
        Test the user search by uid in file
        """
        print_ln('test search users by uid')
        try:
            for user in userdao.search(User(uid="foo*")):
                print_entity(user, "search user")
                print_entity(userdao.read(user), "read user")
        except Exception as e:
            self.fail('user search failed, exception=' + e.msg)

    def test_search_wild(self):
        """
        Test wildcard match
        """
        print_ln('test wildmatch users')
        us = userdao.search(User(uid="test*"))
        try:
            us = sorted(map (lambda u: u.uid, us))
        except Exception as e:
            self.fail('exception '+e.msg)
        if us != ['testuser1', 'testuser2']:
            self.fail('wrong set of users in match: '+dumps(us))

    def test_search_perms(self):
        """
        Test perm search by obj_name in file
        """
        print_ln('test read perms by obj_name')
        try:
            perm = Perm(obj_name="test*")
            p = permdao.read(perm)
            print_entity(p, "Perm")
        except Exception as e:
            self.fail('perm search failed, exception=' + e.msg)

    def test_search_roles(self):
        """
        Test role search by name in file
        """
        print_ln('test search role by name')
        try:
            rs = roledao.search(Role(name="test*"))
            for r in rs:
                print_entity(r, "Role")
        except Exception as e:
            self.fail('role search failed, exception=' + e.msg)

    def test_auth_user(self):
        print_ln('test authentication')
        uids = ['testuser1','testuser2','foouser1']
        for uid in uids:
            for pw in uids:
                exp_res = "success" if uid==pw else "authfail"
                result = None
                try:
                    if userdao.authenticate(userdao.User(uid=uid,password=pw)):
                        result = "success"
                except fileex.AuthFail as a:
                    result = "authfail"
                except fileex.AuthError as a:
                    result = "autherror: "+str(a)
                except Exception as e:
                    result = "exception: "+str(e)
                if result != exp_res:
                    self.fail('user auth: user {} password {} expected {} got {}'
                              .format(uid,pw,exp_res,result))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDaos('test_search_users'))
    suite.addTest(TestDaos('test_search_wild'))
    suite.addTest(TestDaos('test_search_perms'))
    suite.addTest(TestDaos('test_auth_user'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
