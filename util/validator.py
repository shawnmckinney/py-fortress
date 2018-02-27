'''
Created on Feb 24, 2018

@author: smckinn
'''

import abc


class Validator(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    @abc.abstractmethod
    def validate(self, constraint, time):
        pass