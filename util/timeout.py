'''
Created on Feb 24, 2018

@author: smckinn
'''

from util.validator import Validator

class TimeOut(Validator):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def validate(self, constraint, time):
        print('TimeOut.validate time=' + str(time) + ', constraint timeout=' + constraint.timeout)
        