'''
Created on Feb 24, 2018

@author: smckinn
'''

from util.validator import Validator

class Day(Validator):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def validate(self, constraint, time):
        print('Day.validate time=' + str(time) + ', constraint day_mask=' + constraint.day_mask)
        