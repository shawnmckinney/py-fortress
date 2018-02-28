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
        
    def validate(self, constraint, time):
        logger.info('Day.validate time=' + str(time) + ', constraint day_mask=' + constraint.day_mask)
        