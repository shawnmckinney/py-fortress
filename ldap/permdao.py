'''
Created on Feb 16, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

import uuid    
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
from model import Permission, PermObj
from ldap import ldaphelper, LdapException, NotFound, NotUnique
from util import Config, global_ids


def read (entity):
    permList = search(entity)
    if permList is None or len(permList) == 0:
        raise NotFound("Perm Read not found, obj name=" + entity.obj_name + ', op name=' + entity.op_name)    
    elif len(permList) > 1:
        raise NotUnique("Perm Read not unique, obj name=" + entity.obj_name + ', op name=' + entity.op_name)
    else:
        return permList[0]


def search (entity):
    __validate(entity, "Permission Search")
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
        raise LdapException('Perm search error=' + str(e))
    else:        
        if total_entries > 0:
            for entry in response:
                permList.append(__unload(entry))
    finally:
        if conn:        
            ldaphelper.close(conn)
    return permList


def search_objs (entity):
    __validate_obj(entity, "PermObj Search")
    conn = None            
    permList = []
    search_filter = '(&(objectClass=' + PERM_OBJ_OC_NAME + ')'
    search_filter += '(' + OBJ_NM + '=' + entity.obj_name + '))'           
    try:
        conn = ldaphelper.open()
        id = conn.search(search_base, search_filter, attributes=SEARCH_OBJ_ATTRS)
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)        
    except Exception as e:
        raise LdapException('PermObj search error=' + str(e))
    else:        
        if total_entries > 0:
            for entry in response:
                permList.append(__unload_obj(entry))
    finally:
        if conn:        
            ldaphelper.close(conn)
    return permList


# assumes that roles contains at least one role name
def search_on_roles (roles):    
    conn = None            
    permList = []    
    search_filter = '(&(objectClass=' + PERM_OC_NAME + ')'
    if len (roles) > 1:
        search_filter += '(|'
        end_filter = '))'
    else:
        end_filter = ')'
    for role in roles:
        search_filter += '(' + ROLES + '=' + role + ')'
    search_filter += end_filter                    
    try:
        conn = ldaphelper.open()
        id = conn.search(search_base, search_filter, attributes=SEARCH_ATTRS)
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)        
    except Exception as e:
        raise LdapException('Perm Search Roles error=' + str(e))
    else:        
        if total_entries > 0:
            for entry in response:
                permList.append(__unload(entry))
    finally:
        if conn:        
            ldaphelper.close(conn)
    return permList


def __unload(entry):
    entity = Permission()
    entity.dn = ldaphelper.get_dn(entry)
    
    entity.internal_id = ldaphelper.get_attr_val(entry[ATTRIBUTES][global_ids.INTERNAL_ID])
    entity.obj_id = ldaphelper.get_attr_val(entry[ATTRIBUTES][OBJ_ID])
    entity.obj_name = ldaphelper.get_attr_val(entry[ATTRIBUTES][OBJ_NM])
    entity.op_name = ldaphelper.get_attr_val(entry[ATTRIBUTES][OP_NM])
    entity.abstract_name = ldaphelper.get_attr_val(entry[ATTRIBUTES][PERM_NAME])
    entity.type = ldaphelper.get_attr_val(entry[ATTRIBUTES][TYPE])
    entity.description = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][global_ids.DESC])
    # Get the multi-occurring attrs:
    entity.users = ldaphelper.get_list(entry[ATTRIBUTES][USERS])    
    entity.roles = ldaphelper.get_list(entry[ATTRIBUTES][ROLES])
    entity.props = ldaphelper.get_list(entry[ATTRIBUTES][global_ids.PROPS])
    return entity


def __unload_obj(entry):
    entity = PermObj()
    entity.dn = ldaphelper.get_dn(entry)    
    entity.internal_id = ldaphelper.get_attr_val(entry[ATTRIBUTES][global_ids.INTERNAL_ID])
    entity.obj_name = ldaphelper.get_attr_val(entry[ATTRIBUTES][OBJ_NM])
    entity.type = ldaphelper.get_attr_val(entry[ATTRIBUTES][TYPE])
    entity.description = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][global_ids.DESC])
    entity.ou = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][global_ids.OU])    
    entity.props = ldaphelper.get_list(entry[ATTRIBUTES][global_ids.PROPS])
    return entity


def create_obj ( entity ):
    __validate_obj(entity, 'Create PermObj')
    try:
        attrs = {}
        attrs.update( {OBJ_NM : entity.obj_name} )
        # generate random id:
        entity.internal_id = str(uuid.uuid4())
        attrs.update( {global_ids.INTERNAL_ID : entity.internal_id} )        
        attrs.update( {global_ids.OU : entity.ou} )
            
        if entity.description is not None and len(entity.description) > 0 :        
            attrs.update( {global_ids.DESC : entity.description} )

        if entity.type is not None and len(entity.type) > 0 :        
            attrs.update( {TYPE : entity.type} )
            
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : entity.props} )

        conn = ldaphelper.open()        
        id = conn.add(__get_obj_dn(entity), PERM_OBJ_OCS, attrs)
    except Exception as e:
        raise LdapException('PermObj create error=' + str(e), global_ids.PERM_ADD_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.OBJECT_ALREADY_EXISTS:
            raise LdapException('PermObj create failed, already exists:' + entity.name, global_ids.PERM_ADD_FAILED)             
        elif result != 0:
            raise LdapException('PermObj create failed result=' + str(result), global_ids.PERM_ADD_FAILED)                    
    return entity


def update_obj ( entity ):
    __validate_obj(entity, 'Update PermObj')
    try:
        attrs = {}        
        if entity.ou is not None and len(entity.ou) > 0 :        
            attrs.update( {global_ids.OU : [(MODIFY_REPLACE, [entity.ou])]} )
        if entity.description is not None and len(entity.description) > 0 :        
            attrs.update( {global_ids.DESC : [(MODIFY_REPLACE, [entity.description])]} )            
        if entity.type is not None and len(entity.type) > 0 :        
            attrs.update( {TYPE : [(MODIFY_REPLACE, [entity.type])]} )
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : [(MODIFY_REPLACE, entity.props)]} )
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            id = conn.modify(__get_obj_dn(entity), attrs)
    except Exception as e:
        raise LdapException('PermObj update error=' + str(e), global_ids.PERM_UPDATE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise LdapException('PermObj update failed, not found:' + entity.name, global_ids.PERM_UPDATE_FAILED)             
        elif result != 0:
            raise LdapException('PermObj update failed result=' + str(result), global_ids.PERM_UPDATE_FAILED)                    
    return entity


def delete_obj ( entity ):
    __validate_obj(entity, 'Delete PermObj')
    try:
        conn = ldaphelper.open()        
        id = conn.delete(__get_obj_dn(entity))
    except Exception as e:
        raise LdapException('PermObj delete error=' + str(e), global_ids.PERM_DELETE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise LdapException('PermObj delete not found:' + entity.name, global_ids.PERM_DELETE_FAILED)                    
        elif result != 0:
            raise LdapException('PermObj delete failed result=' + str(result), global_ids.PERM_DELETE_FAILED)                    
    return entity


def __validate(entity, op):
    if entity.obj_name is None or len(entity.obj_name) == 0 :
        __raise_exception(op, OBJ_NM)
    if entity.op_name is None or len(entity.op_name) == 0 :
        __raise_exception(op, OP_NM)

                    
def __validate_obj(entity, op):
    if entity.obj_name is None or len(entity.obj_name) == 0 :
        __raise_exception(op, OBJ_NM)

                    
def __raise_exception(operation, field):
    raise LdapException('permdao.' + operation + ' required field missing:' + field)


def __get_obj_dn(entity):
    return OBJ_NM + '=' + entity.obj_name + "," + search_base

PERM_OC_NAME = 'ftOperation'
PERM_OCS = [PERM_OC_NAME, global_ids.PROP_OC_NAME]
PERM_OBJ_OC_NAME = 'ftObject'
PERM_OBJ_OCS = [PERM_OBJ_OC_NAME, global_ids.PROP_OC_NAME]

ROLES = 'ftRoles'
OBJ_ID = 'ftObjId'
OBJ_NM = 'ftObjNm'
OP_NM = 'ftOpNm'
PERM_NAME = 'ftPermName'
USERS = 'ftUsers'
TYPE = 'ftType'

SEARCH_ATTRS = [
    global_ids.INTERNAL_ID, OBJ_NM, OP_NM, PERM_NAME, OBJ_ID, ROLES,
     USERS, TYPE, global_ids.PROPS, global_ids.DESC
     ]

SEARCH_OBJ_ATTRS = [
    global_ids.INTERNAL_ID, OBJ_NM, TYPE, global_ids.PROPS, global_ids.DESC, global_ids.OU
     ]

search_base = Config.get('dit')['perms']
ATTRIBUTES = 'attributes'