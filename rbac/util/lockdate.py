'''
@copyright: 2022 - Symas Corporation
'''

from . import Validator
from .global_ids import ACTV_FAILED_LOCK, SUCCESS

class LockDate(Validator):
        
    def validate(self, constraint, now, session=None):
        if not constraint.begin_lock_date or constraint.begin_lock_date is None or not constraint.end_lock_date or constraint.end_lock_date is None:
            return SUCCESS                
        elif constraint.begin_lock_date == 'none' or constraint.end_lock_date == 'none':
            return SUCCESS                
        elif constraint.begin_lock_date <= now.date <= constraint.end_lock_date:
            return ACTV_FAILED_LOCK
        else:
            return SUCCESS        
        
        