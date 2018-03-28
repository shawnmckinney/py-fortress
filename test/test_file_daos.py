import unittest
from file import userdao
from model import User
from test.utils import print_user, print_role, print_ln, print_entity
import user_test_data

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
            usr = User(uid = "testuser1")
            uList = userdao.search(usr)
            for idx, entity in enumerate(uList) :
                print_user(entity, "User[" + str(idx+1) + "]:")
        except Exception as e:
            self.fail('user search failed, exception=' + e.msg)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDaos('test_search_users'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
