'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from util.validator import Validator
from util.logger import logger
from util.global_ids import CONSTRAINT_DAY_ERROR, SUCCESS

class Day(Validator):
        
    def validate(self, constraint, now):
        if constraint.day_mask == 'all' or not constraint.day_mask or constraint.day_mask is None:
            return SUCCESS                
        if now.day_of_week in constraint.day_mask:
            return SUCCESS
        else:
            return CONSTRAINT_DAY_ERROR        
        
        