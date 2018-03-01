'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from util.validator import Validator
from util.logger import logger

class Time(Validator):
        
    def validate(self, constraint, now):
        logger.debug('Time.validate constraint time=' + now.time + ', begin_time=' + constraint.begin_time + ', end_time=' + constraint.end_time)
        if constraint.begin_time <= now.time <= constraint.end_time:
            return True
        else:
            return False        
