'''
Created on Feb 11, 2018

@author: smckinney
@copyright: 2018 - Symas Corporation
'''

class LdapException(Exception):
    pass

class NotFound(LdapException):
    pass

class NotUnique(LdapException):
    pass

class InvalidCredentials(LdapException):
    pass
