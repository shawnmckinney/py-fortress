'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from util.validator import Validator
from util.logger import logger

class Time(Validator):
        
    def validate(self, constraint, now):
        if not constraint.begin_time or constraint.begin_time is None or not constraint.end_time or constraint.end_time is None:
            return True        
        elif constraint.begin_time == '0000' and constraint.end_time == '0000':
            return True        
        elif constraint.begin_time <= now.time <= constraint.end_time:
            return True
        else:
            return False        
