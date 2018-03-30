'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

import abc


class Validator(object):
        
    @abc.abstractmethod
    def validate(self, constraint, now, session=None):
        pass