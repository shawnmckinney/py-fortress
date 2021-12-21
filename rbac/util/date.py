'''
@copyright: 2022 - Symas Corporation
'''

from . import Validator
from .global_ids import ACTV_FAILED_DATE, SUCCESS

class Date(Validator):
        
    def validate(self, constraint, now, session=None):      
        if not constraint.begin_date or constraint.begin_date is None or not constraint.end_date or constraint.end_date is None:
            return SUCCESS        
        elif constraint.begin_date == 'none' or constraint.end_date == 'none':
            return SUCCESS        
        elif constraint.begin_date <= now.date <= constraint.end_date:
            return SUCCESS
        else:            
            return ACTV_FAILED_DATE