'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from . import Validator
from . import logger
from .global_ids import ACTV_FAILED_TIMEOUT, SUCCESS

class TimeOut(Validator):
    
    def validate(self, constraint, now, session):
        # this is the expected condition for a new session i.e. first ever access:
        if session.last_access is None:
            return SUCCESS
        logger.debug('TimeOut.validate time=' + str(now.time) + ', last access=' + str(session.last_access) + ', constraint timeout=' + str(constraint.timeout))
        rc = ACTV_FAILED_TIMEOUT
        if constraint.timeout == 0:
            rc = SUCCESS
        else:
            elapsed_time = now.seconds - session.last_access.seconds;
            time_limit = constraint.timeout * 60
            if elapsed_time < time_limit  or constraint.timeout == 0:
                rc = SUCCESS
        return rc       