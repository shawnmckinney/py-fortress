'''
@copyright: 2022 - Symas Corporation
'''

from . import Validator
from .global_ids import ACTV_FAILED_DAY, SUCCESS

class Day(Validator):
        
    def validate(self, constraint, now, session=None):
        if constraint.day_mask == 'all' or not constraint.day_mask or constraint.day_mask is None:
            return SUCCESS                
        if now.day_of_week in constraint.day_mask:
            return SUCCESS
        else:
            return ACTV_FAILED_DAY        
        
        