'''
Created on Feb 24, 2018

@author: smckinn
'''

from util.validator import Validator
from util.logger import logger

class Day(Validator):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def validate(self, constraint, now):
        logger.debug('Day.validate constraint day_of_week=' + now.day_of_week + ', day_mask=' + constraint.day_mask)
        if now.day_of_week in constraint.day_mask:
            return True
        else:
            return False        
        
        