'''
Created on Feb 24, 2018

@author: smckinn
'''

from util.validator import Validator
from util.logger import logger

class TimeOut(Validator):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def validate(self, constraint, now):
        logger.debug('TimeOut.validate time=' + now.time + ', constraint timeout=' + constraint.timeout)
        