'''
Created on Feb 16, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
from model import Permission
from ldap import ldaphelper, LdapException, NotFound, NotUnique
from util import Config


def read (entity):
    permList = search(entity)
    if permList is None or len(permList) == 0:
        raise NotFound()
    elif len(permList > 1):
        raise NotUnique()
    else:
        return permList[0]


def search (entity):
    validate(entity, "Permission Search")
    conn = None            
    permList = []
    search_filter = '(&(objectClass=' + PERM_OC_NAME + ')'
    if entity.obj_name is not None and len(entity.obj_name) > 0 :
        search_filter += '(' + OBJ_NM + '=' + entity.obj_name + ')'
    if entity.op_name is not None and len(entity.op_name) > 0 :
        search_filter += '(' + OP_NM + '=' + entity.op_name + ')'
    if entity.obj_id is not None and len(entity.obj_id) > 0 :
        search_filter += '(' + OBJ_ID + '=' + entity.obj_id + ')'
    search_filter += ')'           
    try:
        conn = ldaphelper.open()
        id = conn.search(search_base, search_filter, attributes=SEARCH_ATTRS)
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)        
    except Exception as e:
        raise LdapException('Exception in permdao.search=' + str(e))
    else:        
        if total_entries > 0:
            for entry in response:
                permList.append(unload(entry))
    finally:
        if conn:        
            ldaphelper.close(conn)
    return permList


def unload(entry):
    entity = Permission()
    entity.dn = ldaphelper.get_dn(entry)
    
    entity.internal_id = ldaphelper.get_attr_val(entry[ATTRIBUTES][INTERNAL_ID])
    entity.obj_id = ldaphelper.get_attr_val(entry[ATTRIBUTES][OBJ_ID])
    entity.obj_name = ldaphelper.get_attr_val(entry[ATTRIBUTES][OBJ_NM])
    entity.op_name = ldaphelper.get_attr_val(entry[ATTRIBUTES][OP_NM])
    entity.abstract_name = ldaphelper.get_attr_val(entry[ATTRIBUTES][PERM_NAME])
    entity.type = ldaphelper.get_attr_val(entry[ATTRIBUTES][TYPE])
    entity.description = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][DESC])

    # Get the multi-occurring attrs:
    entity.users = ldaphelper.get_list(entry[ATTRIBUTES][USERS])    
    entity.roles = ldaphelper.get_list(entry[ATTRIBUTES][ROLES])
    entity.props = ldaphelper.get_list(entry[ATTRIBUTES][PROPS])
            
    return entity


def validate(entity, op):
    if entity.obj_name is None or len(entity.obj_name) == 0 :
        raise_exception(op, OBJ_NM)
    if entity.op_name is None or len(entity.op_name) == 0 :
        raise_exception(op, OP_NM)

                    
def raise_exception(operation, field):
    raise LdapException('permdao.' + operation + ' required field missing:' + field)


PERM_OC_NAME = 'ftOperation'
INTERNAL_ID = 'ftid'
ROLES = 'ftRoles'
OBJ_ID = 'ftObjId'
OBJ_NM = 'ftObjNm'
OP_NM = 'ftOpNm'
PERM_NAME = 'ftPermName'
USERS = 'ftUsers'
TYPE = 'ftType'
PROPS = 'ftProps'
DESC = 'description'

SEARCH_ATTRS = [
    INTERNAL_ID, OBJ_NM, OP_NM, PERM_NAME, OBJ_ID, ROLES,
     USERS, TYPE, PROPS, DESC
     ]

search_base = Config.get('dit')['perms']
ATTRIBUTES = 'attributes'