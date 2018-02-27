'''
Created on Feb 24, 2018

@author: smckinn
'''

from util.validator import Validator

class LockDate(Validator):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def validate(self, constraint, time):
        print('LockDate.validate time=' + str(time) + ', constraint begin_lock_date=' + constraint.begin_lock_date + ', end_lock_date=' + constraint.end_lock_date)
        