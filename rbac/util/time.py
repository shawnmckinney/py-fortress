'''
@copyright: 2022 - Symas Corporation
'''

from .validator import Validator
from .global_ids import ACTV_FAILED_TIME, SUCCESS

class Time(Validator):
        
    def validate(self, constraint, now, session=None):
        if not constraint.begin_time or constraint.begin_time is None or not constraint.end_time or constraint.end_time is None:
            return SUCCESS        
        elif constraint.begin_time == '0000' and constraint.end_time == '0000':
            return SUCCESS        
        elif constraint.begin_time <= now.time <= constraint.end_time:
            return SUCCESS
        else:
            return ACTV_FAILED_TIME        
