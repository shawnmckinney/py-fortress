'''
Created on Mar 17, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from model import Role, Constraint
from ldap import ldaphelper, LdapException, NotFound, NotUnique
from util import Config


def read (entity):
    roleList = search(entity)
    if roleList is None or len(roleList) == 0:
        raise NotFound("Role Read not found, name=" + entity.name)    
    elif len(roleList) > 1:
        raise NotUnique("Role Read not unique, name=" + entity.name)
    else:
        return roleList[0]


def search (entity):
    __validate(entity, "Role Search")
    conn = None            
    roleList = []
    search_filter = '(&(objectClass=' + ROLE_OC_NAME + ')'
    search_filter += '(' + ROLE_NAME + '=' + entity.name + '))'
    try:
        conn = ldaphelper.open()
        id = conn.search(search_base, search_filter, attributes=SEARCH_ATTRS)
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)        
    except Exception as e:
        raise LdapException('Role search error=' + str(e))
    else:        
        if total_entries > 0:
            for entry in response:
                roleList.append(__unload(entry))
    finally:
        if conn:        
            ldaphelper.close(conn)
    return roleList


def __unload(entry):
    entity = Role()
    entity.dn = ldaphelper.get_dn(entry)
    
    entity.internal_id = ldaphelper.get_attr_val(entry[ATTRIBUTES][INTERNAL_ID])
    entity.name = ldaphelper.get_attr_val(entry[ATTRIBUTES][ROLE_NAME])
    entity.description = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][DESC])

    # Get the multi-occurring attrs:
    entity.props = ldaphelper.get_list(entry[ATTRIBUTES][PROPS])
            
    # unload raw user constraint:
    entity.constraint = Constraint(ldaphelper.get_attr_val(entry[ATTRIBUTES][CONSTRAINT]))
    return entity


def __validate(entity, op):
    if entity.name is None or len(entity.name) == 0 :
        __raise_exception(op, ROLE_NAME)

                    
def __raise_exception(operation, field):
    raise LdapException('roledao.' + operation + ' required field missing:' + field)


ROLE_OC_NAME = 'ftRls'
INTERNAL_ID = 'ftid'
ROLE_NAME = 'ftRoleName'
CONSTRAINT = 'ftCstr'
PROPS = 'ftProps'
DESC = 'description'
CN = 'cn'


SEARCH_ATTRS = [
    INTERNAL_ID, ROLE_NAME, CONSTRAINT, PROPS, DESC
     ]

search_base = Config.get('dit')['roles']
ATTRIBUTES = 'attributes'