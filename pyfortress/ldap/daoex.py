'''
Created on Feb 11, 2018

@author: smckinney
@copyright: 2018 - Symas Corporation
'''

from ..util import FortressError

class LdapException(FortressError):
 pass

class NotFound(FortressError):
 pass

class NotUnique(FortressError):
 pass

class InvalidCredentials(FortressError):
 pass
