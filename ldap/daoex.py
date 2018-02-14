'''
Created on Feb 11, 2018

@author: smckinney
'''

class LdapException(Exception):
    pass

class NotFound(LdapException):
    pass

class NotUnique(LdapException):
    pass
