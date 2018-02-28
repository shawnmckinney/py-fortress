'''
Created on Feb 24, 2018

@author: smckinn
'''

from util.validator import Validator
from util.logger import logger

class Time(Validator):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def validate(self, constraint, time):
        logger.info('Time.validate time=' + str(time) + ', constraint begin_time=' + constraint.begin_time + ', end_time=' + constraint.end_time)
        