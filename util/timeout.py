'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from util.validator import Validator
from util.logger import logger

class TimeOut(Validator):
        
    def validate(self, constraint, now):
        logger.debug('TimeOut.validate time=' + now.time + ', constraint timeout=' + constraint.timeout)
        