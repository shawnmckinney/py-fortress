'''
Created on Feb 24, 2018

@author: smckinn
'''

from util.validator import Validator
from util.logger import logger

class LockDate(Validator):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def validate(self, constraint, now):
        logger.debug('LockDate.validate constraint date=' + now.date + ', begin_lock_date=' + constraint.begin_lock_date + ', end_lock_date=' + constraint.end_lock_date)
        if constraint.begin_lock_date <= now.date <= constraint.end_lock_date:
            return False
        else:
            return True        
        
        