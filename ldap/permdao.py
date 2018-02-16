'''
Created on Feb 16, 2018

@author: smckinn
'''
# Copyright 2018 - Symas Corporation

from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
from model import Permission
from ldap import ldaphelper, LdapException, NotFound, NotUnique
from util import Config
import logging


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
    if entity.objName is not None and len(entity.objName) > 0 :
        search_filter += '(' + OBJ_NM + '=' + entity.objName + ')'
    if entity.opName is not None and len(entity.opName) > 0 :
        search_filter += '(' + OP_NM + '=' + entity.opName + ')'
    if entity.objId is not None and len(entity.objId) > 0 :
        search_filter += '(' + OBJ_ID + '=' + entity.objId + ')'
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
    
    entity.internalId = ldaphelper.get_attr_val(entry[ATTRIBUTES][INTERNAL_ID])
    entity.objId = ldaphelper.get_attr_val(entry[ATTRIBUTES][OBJ_ID])
    entity.objName = ldaphelper.get_attr_val(entry[ATTRIBUTES][OBJ_NM])
    entity.opName = ldaphelper.get_attr_val(entry[ATTRIBUTES][OP_NM])
    entity.abstractName = ldaphelper.get_attr_val(entry[ATTRIBUTES][PERM_NAME])
    entity.type = ldaphelper.get_attr_val(entry[ATTRIBUTES][TYPE])
    entity.description = ldaphelper.get_attr_val(entry[ATTRIBUTES][DESC])

    # Get the multi-occurring attrs:
    entity.users = ldaphelper.get_list(entry[ATTRIBUTES][USERS])    
    entity.roles = ldaphelper.get_list(entry[ATTRIBUTES][ROLES])
    entity.props = ldaphelper.get_list(entry[ATTRIBUTES][PROPS])
            
    return entity


def validate(entity, op):
    if entity.objName is None or len(entity.objName) == 0 :
        raise_exception(op, OBJ_NM)
    if entity.opName is None or len(entity.opName) == 0 :
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

ATTRIBUTES = 'attributes'
SEARCH_ATTRS = Config.get('schema')['permission']['attributes']
search_base = Config.get('dit')['perms']