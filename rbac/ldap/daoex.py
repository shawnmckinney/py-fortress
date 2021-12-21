'''
@copyright: 2022 - Symas Corporation
'''

from rbac.util.fortress_error import RbacError

class LdapException(RbacError):
 pass

class NotFound(RbacError):
 pass

class NotUnique(RbacError):
 pass

class InvalidCredentials(RbacError):
 pass
