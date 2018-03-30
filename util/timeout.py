'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from util.validator import Validator
from util.logger import logger
from util.global_ids import ACTV_FAILED_TIMEOUT, SUCCESS

class TimeOut(Validator):
    
    def validate(self, constraint, now, session):
        logger.debug('TimeOut.validate time=' + str(now.time) + ', last access=' + str(session.last_access) + ', constraint timeout=' + str(constraint.timeout))
        rc = ACTV_FAILED_TIMEOUT
        last_time = session.last_access.seconds
        if last_time == 0 or constraint.timeout == 0:
            rc = SUCCESS
        else:
            elapsed_time = now.seconds - last_time;
            time_limit = constraint.timeout * 60
            if elapsed_time < time_limit  or constraint.timeout == 0:
                rc = SUCCESS
        return rc       