'''
Created on Mar 17, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

import uuid
from ldap3 import MODIFY_REPLACE, MODIFY_ADD, MODIFY_DELETE
from ..model import Role, Constraint
from ..ldap import ldaphelper, NotFound, NotUnique
from ..ldap import userdao
from ..util import global_ids
from ..util import FortressError

def read (entity):
    roleList = search(entity)
    if roleList is None or len(roleList) == 0:
        raise NotFound(msg="Role Read not found, name=" + entity.name, id=global_ids.ROLE_NOT_FOUND)    
    elif len(roleList) > 1:
        raise NotUnique(msg="Role Read not unique, name=" + entity.name, id=global_ids.ROLE_READ_FAILED)
    else:
        return roleList[0]


def search (entity):
    conn = None            
    roleList = []
    search_filter = '(&(objectClass=' + ROLE_OC_NAME + ')'
    search_filter += '(' + ROLE_NAME + '=' + entity.name + '))'
    try:
        conn = ldaphelper.open()
        id = conn.search(__CONTAINER_DN, search_filter, attributes=SEARCH_ATTRS)
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)        
    except Exception as e:
        raise FortressError(msg='Role search error=' + str(e), id=global_ids.ROLE_SEARCH_FAILED)
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
    entity.internal_id = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][global_ids.INTERNAL_ID])
    entity.name = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][ROLE_NAME])
    entity.description = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][global_ids.DESC])
    # Get the multi-occurring attrs:
    entity.props = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][global_ids.PROPS])
    entity.members = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][MEMBER])    
    # unload raw constraint:
    entity.constraint = Constraint(ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][global_ids.CONSTRAINT]))
    return entity


def create ( entity ):
    try:
        attrs = {}
        attrs.update( {global_ids.CN : entity.name} )
        attrs.update( {ROLE_NAME : entity.name} )
        # generate random id:
        entity.internal_id = str(uuid.uuid4())
        attrs.update( {global_ids.INTERNAL_ID : entity.internal_id} )        

        # string:
        if entity.description:        
            attrs.update( {global_ids.DESC : entity.description} )
        # list of strings
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : entity.props} )
        # list of comma delimited strings:
        if entity.constraint is None:
            entity.constraint = Constraint(name=entity.name)
        #if entity.constraint is not None:        
        attrs.update( {global_ids.CONSTRAINT : entity.constraint.get_raw()} )
            
        conn = ldaphelper.open()        
        id = conn.add(__get_dn(entity), ROLE_OCS, attrs)
    except Exception as e:
        raise FortressError(msg='Role create error=' + str(e), id=global_ids.ROLE_ADD_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.OBJECT_ALREADY_EXISTS:
            raise NotUnique(msg='Role create failed, already exists:' + entity.name, id=global_ids.ROLE_ADD_FAILED)             
        elif result != 0:
            raise FortressError(msg='Role create failed result=' + str(result), id=global_ids.ROLE_ADD_FAILED)                    
    return entity


def update ( entity ):
    try:
        attrs = {}
        if entity.description:        
            attrs.update( {global_ids.DESC : [(MODIFY_REPLACE, [entity.description])]} )
        # list of srings:
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : [(MODIFY_REPLACE, [entity.props])]} )
        # list of comma delimited strings:
        if entity.constraint is not None :        
            attrs.update( {global_ids.CONSTRAINT : [(MODIFY_REPLACE, [entity.constraint.get_raw()])]} )
        if len(attrs) > 0:
            conn = ldaphelper.open()        
            id = conn.modify(__get_dn(entity), attrs)        
    except Exception as e:
        raise FortressError(msg='Role update error=' + str(e), id=global_ids.ROLE_UPDATE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='Role update failed, not found:' + entity.name, id=global_ids.ROLE_NOT_FOUND)             
        elif result != 0:
            raise FortressError('Role update failed result=' + str(result), global_ids.ROLE_UPDATE_FAILED)                    
    return entity


def delete ( entity ):
    try:
        conn = ldaphelper.open()        
        id = conn.delete(__get_dn(entity))
    except Exception as e:
        raise FortressError(msg='Role delete error=' + str(e), id=global_ids.ROLE_DELETE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='Role delete not found:' + entity.name, id=global_ids.ROLE_NOT_FOUND)                    
        elif result != 0:
            raise FortressError(msg='Role delete failed result=' + str(result), id=global_ids.ROLE_DELETE_FAILED)                    
    return entity


def add_member ( entity, uid ):    
    try:        
        attrs = {}
        if uid:
            user_dn = __get_user_dn(uid)            
            attrs.update( {MEMBER : [(MODIFY_ADD, user_dn)]} )
            conn = ldaphelper.open()        
            id = conn.modify(__get_dn(entity), attrs)
    except Exception as e:
        raise FortressError(msg='Add member error=' + str(e), id=global_ids.ROLE_USER_ASSIGN_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='Add member failed, not found, role=' +  entity.name + ', member dn=' + user_dn, id=global_ids.ROLE_NOT_FOUND)             
        elif result != 0:
            raise FortressError(msg='Add member failed result=' + str(result), id=global_ids.ROLE_USER_ASSIGN_FAILED)                    
    return entity


def remove_member ( entity, uid ):    
    try:        
        attrs = {}
        if uid:
            user_dn = __get_user_dn(uid)
            attrs.update( {MEMBER : [(MODIFY_DELETE, user_dn)]} )
            conn = ldaphelper.open()        
            id = conn.modify(__get_dn(entity), attrs)
    except Exception as e:
        raise FortressError(msg='Remove member error=' + str(e), id=global_ids.ROLE_REMOVE_OCCUPANT_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NO_SUCH_ATTRIBUTE:
            raise FortressError(msg='Remove member failed, not assigned, role=' +  entity.name + ', member dn=' + user_dn, id=global_ids.URLE_ASSIGN_NOT_EXIST)             
        elif result != 0:
            raise FortressError(msg='Remove member failed result=' + str(result), id=global_ids.ROLE_REMOVE_OCCUPANT_FAILED)                    
    return entity


def get_members (entity):
    conn = None            
    uList = []
    search_filter = '(&(objectClass=' + ROLE_OC_NAME + ')'
    search_filter += '(' + ROLE_NAME + '=' + entity.name + '))'
    try:
        conn = ldaphelper.open()
        id = conn.search(__CONTAINER_DN, search_filter, attributes=[MEMBER])
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)
    except Exception as e:
        raise FortressError(msg='Get members search error=' + str(e), id=global_ids.ROLE_OCCUPANT_SEARCH_FAILED)
    else:
        if total_entries == 0:
            raise NotFound(msg="Role not found, name=" + entity.name, id=global_ids.ROLE_NOT_FOUND)    
        elif total_entries > 1:
            raise NotUnique(msg="Role not unique, name=" + entity.name, id=global_ids.ROLE_SEARCH_FAILED)        
        member_dns = ldaphelper.get_list(response[0][global_ids.ATTRIBUTES][MEMBER])
        uList = __convert_list(member_dns)
    finally:
        if conn:        
            ldaphelper.close(conn)
    return uList


def get_members_constraint (entity):
    conn = None            
    mList = []
    search_filter = '(&(objectClass=' + ROLE_OC_NAME + ')'
    search_filter += '(' + ROLE_NAME + '=' + entity.name + '))'
    try:
        conn = ldaphelper.open()
        id = conn.search(__CONTAINER_DN, search_filter, attributes=[MEMBER, global_ids.CONSTRAINT])
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)
    except Exception as e:
        raise FortressError(msg='Get members search error=' + str(e), id=global_ids.ROLE_OCCUPANT_SEARCH_FAILED)
    else:
        if total_entries == 0:
            raise NotFound(msg="Role not found, name=" + entity.name, id=global_ids.ROLE_NOT_FOUND)    
        elif total_entries > 1:
            raise NotUnique(msg="Role not unique, name=" + entity.name, id=global_ids.ROLE_SEARCH_FAILED)        
        member_dns = ldaphelper.get_list(response[0][global_ids.ATTRIBUTES][MEMBER])
        constraint = Constraint(ldaphelper.get_attr_val(response[0][global_ids.ATTRIBUTES][global_ids.CONSTRAINT]))        
        mList = __convert_list(member_dns)
    finally:
        if conn:        
            ldaphelper.close(conn)
    return [mList, constraint]


def __get_dn(entity):
    return global_ids.CN + '=' + entity.name + "," + __CONTAINER_DN


def __get_user_dn(uid):
    # TODO: find a better way to do this:
    return global_ids.UID + '=' + uid + ',' + userdao.CONTAINER_DN


def __convert_list(list_dns):
    list_uids = []
    for member_dn in list_dns:
        list_uids.append(__get_user_id(member_dn))
    return list_uids


def __get_user_id(user_dn):
    uid = None    
    values = user_dn.split(',')        
    values = [ val.strip() for val in values ]
    if values[0] is not None:
        uid=values[0]
    return uid[4:]    
    

ROLE_OC_NAME = 'ftRls'
ROLE_OCS = [ROLE_OC_NAME, global_ids.PROP_OC_NAME]
ROLE_NAME = 'ftRoleName'
MEMBER = 'roleOccupant'

SEARCH_ATTRS = [
    global_ids.INTERNAL_ID, ROLE_NAME, global_ids.CONSTRAINT, global_ids.PROPS, global_ids.DESC, MEMBER
     ]

__CONTAINER_DN = ldaphelper.get_container_dn(global_ids.ROLE_OU)