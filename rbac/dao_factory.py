'''
@copyright: 2022 - Symas Corporation

Backend factory to select the appropriate data access layer based on configuration.
'''

from rbac.util import Config

def get_dao_backend():
    """
    Get the configured backend type (ldap, sql, or file)
    """
    return Config.getDefault('backend', 'ldap')

def get_userdao():
    """
    Get the user DAO implementation based on configuration
    """
    backend = get_dao_backend()
    
    if backend == 'sql':
        from rbac.sql import userdao
        return userdao
    elif backend == 'file':
        from rbac.file import userdao
        return userdao
    else:  # default to ldap
        from rbac.ldap import userdao
        return userdao

def get_roledao():
    """
    Get the role DAO implementation based on configuration
    """
    backend = get_dao_backend()
    
    if backend == 'sql':
        from rbac.sql import roledao
        return roledao
    elif backend == 'file':
        from rbac.file import roledao
        return roledao
    else:  # default to ldap
        from rbac.ldap import roledao
        return roledao

def get_permdao():
    """
    Get the permission DAO implementation based on configuration
    """
    backend = get_dao_backend()
    
    if backend == 'sql':
        from rbac.sql import permdao
        return permdao
    elif backend == 'file':
        from rbac.file import permdao
        return permdao
    else:  # default to ldap
        from rbac.ldap import permdao
        return permdao