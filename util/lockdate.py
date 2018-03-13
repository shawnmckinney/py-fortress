'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from util.validator import Validator
from util.logger import logger

class LockDate(Validator):
        
    def validate(self, constraint, now):
        if not constraint.begin_lock_date or constraint.begin_lock_date is None or not constraint.end_lock_date or constraint.end_lock_date is None:
            return True                
        elif constraint.begin_lock_date == 'none' or constraint.end_lock_date == 'none':
            return True                
        elif constraint.begin_lock_date <= now.date <= constraint.end_lock_date:
            return False
        else:
            return True        
        
        