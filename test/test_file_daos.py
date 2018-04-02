import unittest
from file import userdao,permdao
from model import User,Perm
from test.utils import print_user, print_role, print_ln, print_entity
import user_test_data
from json import dumps

class BasicTestSuite(unittest.TestCase):
    """These tests assume fortress user and permission data has been pre-loaded into File, i.e. via apache fortress administrative functions."""

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
            usr = User(uid = "foo*")
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :
                print_entity(entity, "User[" + str(idx+1) + "]:")
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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDaos('test_search_users'))
    suite.addTest(TestDaos('test_search_wild'))
    suite.addTest(TestDaos('test_search_perms'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
