'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

import unittest
from pyfortress.util import Date
from pyfortress.util import Day
from pyfortress.util import LockDate
from pyfortress.util import Time
from pyfortress.util import TimeOut
from pyfortress.util import CurrentDateTime
from pyfortress.model import Constraint
from pyfortress.test import print_ln, print_entity

cons1 = [
    Constraint(
        name='foo1',
        timeout='0',
        begin_time='0100',
        end_time='2400',
        begin_date='20170101',
        end_date='20171231',
        begin_lock_date='20170101',
        end_lock_date='20171231',
        day_mask='1234567',
        ),
    Constraint(
        name='foo2',
        timeout='0',
        begin_time='0100',
        end_time='2400',
        begin_date='20170101',
        end_date='20171231',
        begin_lock_date='20180101',
        end_lock_date='20181231',
        day_mask='1234567',
        ),
    Constraint(
        name='foo3',
        timeout='0',
        begin_time='0100',
        end_time='2400',
        begin_date='20170101',
        end_date='20181231',
        begin_lock_date='20170101',
        end_lock_date='20171231',
        day_mask='1234567',
        ),
    ]

class BasicTestSuite(unittest.TestCase):
    """Verify the temporal validators against the current system date with some sample constraint values."""
                
class TestConstraints(unittest.TestCase):
    
        
    def test_validators(self):
        """
        Test the temporal constraints
        """
        print('test time-based constraints')
        validators = []
        validators.append(Date())
        validators.append(Day())
        validators.append(LockDate())
        validators.append(Time())
        validators.append(TimeOut())
        for constraint in cons1:
            for validator in validators:
                result = validator.validate(constraint, CurrentDateTime())
                print_entity (constraint, "Validate" + str(validator))
                print_ln( 'result=' + str(result), 1 )
    

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestConstraints('test_validators'))
    return suite  


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())


if __name__ == "__main__":
    unittest.main()