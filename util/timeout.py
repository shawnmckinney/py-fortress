'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from util.validator import Validator
from util.logger import logger
from util.global_ids import ACTV_FAILED_TIMEOUT, SUCCESS

class TimeOut(Validator):
        
    def validate(self, constraint, now):
        logger.debug('TimeOut.validate time=' + now.time + ', constraint timeout=' + constraint.timeout)
        # Todo: until implemented, return False:
        return ACTV_FAILED_TIMEOUT
        