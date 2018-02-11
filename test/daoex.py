'''
Created on Feb 11, 2018

@author: smckinney
'''

class FortressException(Exception):
    pass

class NotFound(FortressException):
    pass

class NotUnique(FortressException):
    pass
