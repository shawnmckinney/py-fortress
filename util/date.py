'''
Created on Feb 24, 2018

@author: smckinn
'''

from util.validator import Validator

class Date(Validator):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def validate(self, constraint, time):
        print('Date.validate time=' + str(time) + ', constraint begin_date=' + constraint.begin_date + ', end_date=' + constraint.end_date)
        