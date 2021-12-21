'''
@copyright: 2022 - Symas Corporation
'''

import abc


class Validator(object):
        
    @abc.abstractmethod
    def validate(self, constraint, now, session=None):
        pass