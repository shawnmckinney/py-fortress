'''
Created on Feb 16, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

import uuid    
from ldap3 import MODIFY_REPLACE, MODIFY_ADD, MODIFY_DELETE
from ..model import Perm, PermObj
from ..ldap import ldaphelper, NotFound, NotUnique
from ..util import global_ids
from ..util import FortressError


def read (entity):
    permList = search(entity)
    if permList is None or len(permList) == 0:
        raise NotFound(msg="Perm Read not found, obj name=" + entity.obj_name + ', op name=' + entity.op_name, id=global_ids.PERM_NOT_EXIST)    
    elif len(permList) > 1:
        raise NotUnique(msg="Perm Read not unique, obj name=" + entity.obj_name + ', op name=' + entity.op_name, id=global_ids.PERM_READ_OP_FAILED)
    else:
        return permList[0]


def search (entity):
    conn = None            
    permList = []
    search_filter = '(&(objectClass=' + PERM_OC_NAME + ')'
    if entity.obj_name:
        search_filter += '(' + OBJ_NM + '=' + entity.obj_name + ')'
    if entity.op_name:
        search_filter += '(' + OP_NM + '=' + entity.op_name + ')'
    if entity.obj_id:
        search_filter += '(' + OBJ_ID + '=' + entity.obj_id + ')'
    search_filter += ')'           
    try:
        conn = ldaphelper.open()
        id = conn.search(__CONTAINER_DN, search_filter, attributes=SEARCH_ATTRS)
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)        
    except Exception as e:
        raise FortressError(msg='Perm search error=' + str(e), id=global_ids.PERM_SEARCH_FAILED)
    else:        
        if total_entries > 0:
            for entry in response:
                permList.append(__unload(entry))
    finally:
        if conn:        
            ldaphelper.close(conn)
    return permList


def read_obj (entity):
    objList = search_objs(entity)
    if objList is None or len(objList) == 0:
        raise NotFound(msg="PermObj Read not found, obj name=" + entity.obj_name, id=global_ids.PERM_OBJ_NOT_FOUND)    
    elif len(objList) > 1:
        raise NotUnique(msg="PermObj Read not unique, obj name=" + entity.obj_name, id=global_ids.PERM_READ_OBJ_FAILED)
    else:
        return objList[0]


def search_objs (entity):
    conn = None            
    permList = []
    search_filter = '(&(objectClass=' + PERM_OBJ_OC_NAME + ')'
    search_filter += '(' + OBJ_NM + '=' + entity.obj_name + '))'           
    try:
        conn = ldaphelper.open()
        id = conn.search(__CONTAINER_DN, search_filter, attributes=SEARCH_OBJ_ATTRS)
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)        
    except Exception as e:
        raise FortressError(msg='PermObj search error=' + str(e), id=global_ids.PERM_SEARCH_FAILED)
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
        id = conn.search(__CONTAINER_DN, search_filter, attributes=SEARCH_ATTRS)
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)        
    except Exception as e:
        raise FortressError(msg='Perm Search Roles error=' + str(e), id=global_ids.PERM_ROLE_SEARCH_FAILED)
    else:        
        if total_entries > 0:
            for entry in response:
                permList.append(__unload(entry))
    finally:
        if conn:        
            ldaphelper.close(conn)
    return permList


def __unload(entry):
    entity = Perm()
    entity.dn = ldaphelper.get_dn(entry)
    
    entity.internal_id = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][global_ids.INTERNAL_ID])
    entity.obj_id = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][OBJ_ID])
    entity.obj_name = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][OBJ_NM])
    entity.op_name = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][OP_NM])
    entity.abstract_name = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][PERM_NAME])
    entity.type = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][TYPE])
    entity.description = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][global_ids.DESC])
    # Get the multi-occurring attrs:
    entity.users = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][USERS])    
    entity.roles = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][ROLES])
    entity.props = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][global_ids.PROPS])
    return entity


def __unload_obj(entry):
    entity = PermObj()
    entity.dn = ldaphelper.get_dn(entry)    
    entity.internal_id = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][global_ids.INTERNAL_ID])
    entity.obj_name = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][OBJ_NM])
    entity.type = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][TYPE])
    entity.description = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][global_ids.DESC])
    entity.ou = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][global_ids.OU])    
    entity.props = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][global_ids.PROPS])
    return entity


def create ( entity ):
    try:
        attrs = {}
        attrs.update( {OBJ_NM : entity.obj_name} )
        attrs.update( {OP_NM : entity.op_name} )
        entity.abstract_name = entity.obj_name + '.' + entity.op_name        
        attrs.update( {global_ids.CN : entity.abstract_name} )
                
        # generate random id:
        entity.internal_id = str(uuid.uuid4())
        attrs.update( {global_ids.INTERNAL_ID : entity.internal_id} )
        if entity.obj_id:        
            attrs.update( {OBJ_ID : entity.obj_id} )
        if entity.description:        
            attrs.update( {global_ids.DESC : entity.description} )
        if entity.abstract_name:        
            attrs.update( {PERM_NAME : entity.abstract_name} )
        if entity.type:        
            attrs.update( {TYPE : entity.type} )
        # list of strings:
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : entity.props} )            
        if entity.users is not None and len(entity.users) > 0 :        
            attrs.update( {USERS : entity.users} )        
        if entity.roles is not None and len(entity.roles) > 0 :        
            attrs.update( {ROLES : entity.roles} )
        conn = ldaphelper.open()        
        id = conn.add(__get_dn(entity), PERM_OCS, attrs)
    except Exception as e:
        raise FortressError(msg='Perm create error=' + str(e), id=global_ids.PERM_ADD_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.OBJECT_ALREADY_EXISTS:
            raise NotUnique(msg='Perm create failed, already exists:' + entity.obj_name, id=global_ids.PERM_ADD_FAILED)             
        elif result != 0:
            raise FortressError(msg='Perm create failed result=' + str(result), id=global_ids.PERM_ADD_FAILED)                    
    return entity


def update ( entity ):
    try:
        attrs = {}
        if entity.description:        
            attrs.update( {global_ids.DESC : [(MODIFY_REPLACE, [entity.description])]} )            
        if entity.type:        
            attrs.update( {TYPE : [(MODIFY_REPLACE, [entity.type])]} )
        # list of strings:
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : [(MODIFY_REPLACE, entity.props)]} )
        if entity.users is not None and len(entity.users) > 0 :        
            attrs.update( {USERS : [(MODIFY_REPLACE, entity.users)]} )        
        if entity.roles is not None and len(entity.roles) > 0 :        
            attrs.update( {ROLES : [(MODIFY_REPLACE, entity.roles)]} )
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            id = conn.modify(__get_dn(entity), attrs)
    except Exception as e:
        raise FortressError(msg='Perm update error=' + str(e), id=global_ids.PERM_UPDATE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='Perm update failed, not found:' + entity.obj_name, id=global_ids.PERM_OP_NOT_FOUND)             
        elif result != 0:
            raise FortressError(msg='Perm update failed result=' + str(result), id=global_ids.PERM_UPDATE_FAILED)                    
    return entity


def delete ( entity ):
    try:
        conn = ldaphelper.open()        
        id = conn.delete(__get_dn(entity))
    except Exception as e:
        raise FortressError(msg='Perm delete error=' + str(e), id=global_ids.PERM_DELETE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='Perm delete not found:' + entity.obj_name, id=global_ids.PERM_OP_NOT_FOUND)                    
        elif result != 0:
            raise FortressError(msg='Perm delete failed result=' + str(result), id=global_ids.PERM_DELETE_FAILED)                    
    return entity


def grant ( entity, role ):
    try:
        attrs = {}
        # constraint type:
        if role is not None:
            attrs.update( {ROLES : [(MODIFY_ADD, role.name)]} )                                     
            conn = ldaphelper.open()                
            id = conn.modify(__get_dn(entity), attrs)
    except Exception as e:
        raise FortressError(msg='Perm grant error=' + str(e), id=global_ids.PERM_GRANT_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='Perm grant failed, not found, obj name=' 
                                +  entity.obj_name + ', op_name=' 
                                + entity.op_name 
                                + ', op id=' + entity.obj_id 
                                + ', role='+ role.name, 
                                id=global_ids.PERM_OP_NOT_FOUND)             
        elif result != 0:
            raise FortressError(msg='Perm grant failed result=' + str(result), id=global_ids.PERM_GRANT_FAILED)                    
    return entity


def revoke ( entity, role ):
    try:
        attrs = {}
        # constraint type:
        if role is not None:
            attrs.update( {ROLES : [(MODIFY_DELETE, role.name)]} )                                     
            conn = ldaphelper.open()                
            id = conn.modify(__get_dn(entity), attrs)
    except Exception as e:
        raise FortressError(msg='Perm revoke error=' + str(e), id=global_ids.PERM_REVOKE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NO_SUCH_ATTRIBUTE:
            raise FortressError(msg='Perm revoke failed, not granted, obj name=' 
                                +  entity.obj_name 
                                + ', op_name=' 
                                + entity.op_name 
                                + ', role='
                                + role.name, 
                                id=global_ids.PERM_ROLE_NOT_EXIST)            
        elif result == global_ids.NOT_FOUND:
            raise FortressError(msg='Perm not found, obj name=' 
                                +  entity.obj_name 
                                + ', op_name=' 
                                + entity.op_name 
                                + ', role='
                                + role.name, 
                                id=global_ids.PERM_NOT_EXIST)            
        elif result != 0:
            raise FortressError(msg='Perm revoke failed result=' + str(result), id=global_ids.PERM_REVOKE_FAILED)                    
    return entity


def create_obj ( entity ):
    try:
        attrs = {}
        attrs.update( {OBJ_NM : entity.obj_name} )
        # generate random id:
        entity.internal_id = str(uuid.uuid4())
        attrs.update( {global_ids.INTERNAL_ID : entity.internal_id} )
        # ou is req'd for organizationalUnit object class, if caller did not set, use obj name.
        if not entity.ou:
            entity.ou = entity.obj_name
        attrs.update( {global_ids.OU : entity.ou} )
        if entity.description:        
            attrs.update( {global_ids.DESC : entity.description} )
        if entity.type:        
            attrs.update( {TYPE : entity.type} )
        # list of comma delimited strings:
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : entity.props} )
        conn = ldaphelper.open()        
        id = conn.add(__get_obj_dn(entity), PERM_OBJ_OCS, attrs)
    except Exception as e:
        raise FortressError(msg='PermObj create error=' + str(e), id=global_ids.PERM_ADD_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.OBJECT_ALREADY_EXISTS:
            raise NotUnique(msg='PermObj create failed, already exists:' + entity.obj_name, id=global_ids.PERM_DUPLICATE)             
        elif result != 0:
            raise FortressError(msg='PermObj create failed result=' + str(result), id=global_ids.PERM_ADD_FAILED)                    
    return entity


def update_obj ( entity ):
    conn = None
    id = 0
    try:
        attrs = {}        
        if entity.ou:        
            attrs.update( {global_ids.OU : [(MODIFY_REPLACE, [entity.ou])]} )
        if entity.description:        
            attrs.update( {global_ids.DESC : [(MODIFY_REPLACE, [entity.description])]} )            
        if entity.type:        
            attrs.update( {TYPE : [(MODIFY_REPLACE, [entity.type])]} )
        # list of comma delimited strings:
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : [(MODIFY_REPLACE, entity.props)]} )
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            id = conn.modify(__get_obj_dn(entity), attrs)
    except Exception as e:
        raise FortressError(msg='PermObj update error=' + str(e), id=global_ids.PERM_UPDATE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='PermObj update failed, not found:' + entity.obj_name, id=global_ids.PERM_OBJ_NOT_FOUND)             
        elif result != 0:
            raise FortressError(msg='PermObj update failed result=' + str(result), id=global_ids.PERM_UPDATE_FAILED)                    
    return entity


def delete_obj ( entity ):
    try:
        conn = ldaphelper.open()        
        id = conn.delete(__get_obj_dn(entity))
    except Exception as e:
        raise FortressError(msg='PermObj delete error=' + str(e), id=global_ids.PERM_DELETE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='PermObj delete not found:' + entity.obj_name, id=global_ids.PERM_OBJ_NOT_FOUND)
        elif result == global_ids.NOT_ALLOWED_ON_NONLEAF:
            raise FortressError(msg='PermObj has children.', id=global_ids.PERM_OBJECT_DELETE_FAILED_NONLEAF)                                
        elif result != 0:
            raise FortressError(msg='PermObj delete failed result=' + str(result), id=global_ids.PERM_DELETE_FAILED)                    
    return entity


def __get_obj_dn(entity):
    return OBJ_NM + '=' + entity.obj_name + "," + __CONTAINER_DN


def __get_dn(entity):
    dn = ''
    if entity.obj_id is not None and len(entity.obj_id) > 0:
        dn = OBJ_ID + '=' + entity.obj_id + '+' + OP_NM + '=' + entity.op_name + ',' + __get_obj_dn(entity)
    else:
        dn = OP_NM + '=' + entity.op_name + ',' + __get_obj_dn(entity)
    return dn


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

__CONTAINER_DN = ldaphelper.get_container_dn(global_ids.PERM_OU)