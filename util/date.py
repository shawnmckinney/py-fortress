'''
Created on Feb 24, 2018

@author: smckinn
'''

from util.validator import Validator
from util.logger import logger

class Date(Validator):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def validate(self, constraint, now):
        logger.debug('Date.validate constraint date=' + now.date + ', begin_date=' + constraint.begin_date + ', end_date=' + constraint.end_date)
        if constraint.begin_date <= now.date <= constraint.end_date:
            return True
        else:
            return False        
        