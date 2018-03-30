import unittest
from file import userdao
from model import User
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
                print_user(entity, "User[" + str(idx+1) + "]:")
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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDaos('test_search_users'))
    suite.addTest(TestDaos('test_search_wild'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
