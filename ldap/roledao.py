'''
Created on Mar 17, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

import uuid
from model import Role, Constraint
from ldap import ldaphelper, LdapException, NotFound, NotUnique
from ldap3 import MODIFY_REPLACE, MODIFY_ADD, MODIFY_DELETE
from util import Config, global_ids
from ldap import userdao


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
    entity.internal_id = ldaphelper.get_attr_val(entry[ATTRIBUTES][global_ids.INTERNAL_ID])
    entity.name = ldaphelper.get_attr_val(entry[ATTRIBUTES][ROLE_NAME])
    entity.description = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][global_ids.DESC])
    # Get the multi-occurring attrs:
    entity.props = ldaphelper.get_list(entry[ATTRIBUTES][global_ids.PROPS])
    # unload raw constraint:
    entity.constraint = Constraint(ldaphelper.get_attr_val(entry[ATTRIBUTES][global_ids.CONSTRAINT]))
    return entity


def create ( entity ):
    __validate(entity, 'Create Role')
    try:
        attrs = {}
        attrs.update( {global_ids.CN : entity.name} )
        attrs.update( {ROLE_NAME : entity.name} )
        # generate random id:
        entity.internal_id = str(uuid.uuid4())
        attrs.update( {global_ids.INTERNAL_ID : entity.internal_id} )        

        if entity.description is not None and len(entity.description) > 0 :        
            attrs.update( {global_ids.DESC : entity.description} )

        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : entity.props} )

        if entity.constraint is not None :        
            attrs.update( {global_ids.CONSTRAINT : entity.constraint.get_raw()} )

        conn = ldaphelper.open()        
        id = conn.add(__get_dn(entity), ROLE_OCS, attrs)
    except Exception as e:
        raise LdapException('Role create error=' + str(e), global_ids.ROLE_ADD_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.OBJECT_ALREADY_EXISTS:
            raise LdapException('Role create failed, already exists:' + entity.name, global_ids.ROLE_ADD_FAILED)             
        elif result != 0:
            raise LdapException('Role create failed result=' + str(result), global_ids.ROLE_ADD_FAILED)                    
    return entity


def update ( entity ):
    __validate(entity, 'Update Role')
    try:
        attrs = {}
        if entity.description is not None and len(entity.description) > 0 :        
            attrs.update( {global_ids.DESC : [(MODIFY_REPLACE, [entity.description])]} )

        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : [(MODIFY_REPLACE, [entity.props])]} )

        if entity.constraint is not None :        
            attrs.update( {global_ids.CONSTRAINT : [(MODIFY_REPLACE, [entity.constraint.get_raw()])]} )

        if len(attrs) > 0:
            conn = ldaphelper.open()        
            id = conn.modify(__get_dn(entity), attrs)        
    except Exception as e:
        raise LdapException('Role update error=' + str(e), global_ids.ROLE_UPDATE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise LdapException('Role update failed, not found:' + entity.name, global_ids.ROLE_UPDATE_FAILED)             
        elif result != 0:
            raise LdapException('Role update failed result=' + str(result), global_ids.ROLE_UPDATE_FAILED)                    
    return entity


def delete ( entity ):
    __validate(entity, 'Delete Role')
    try:
        conn = ldaphelper.open()        
        id = conn.delete(__get_dn(entity))
    except Exception as e:
        raise LdapException('Role delete error=' + str(e), global_ids.ROLE_DELETE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise LdapException('Role delete not found:' + entity.name, global_ids.ROLE_DELETE_FAILED)                    
        elif result != 0:
            raise LdapException('Role delete failed result=' + str(result), global_ids.ROLE_DELETE_FAILED)                    
    return entity


def add_member ( entity, uid ):    
    __validate(entity, 'Add Member')
    try:        
        attrs = {}
        if uid is not None and len(uid) > 0 :
            user_dn = __get_user_dn(uid)            
            attrs.update( {MEMBER : [(MODIFY_ADD, user_dn)]} )
            conn = ldaphelper.open()        
            id = conn.modify(__get_dn(entity), attrs)
    except Exception as e:
        raise LdapException('Add member error=' + str(e), global_ids.ROLE_USER_ASSIGN_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise LdapException('Add member failed, not found, role=' +  entity.name + ', member dn=' + user_dn)             
        elif result != 0:
            raise LdapException('Add member failed result=' + str(result), global_ids.ROLE_USER_ASSIGN_FAILED)                    
    return entity


def remove_member ( entity, uid ):    
    __validate(entity, 'Remove Member')
    try:        
        attrs = {}
        if uid is not None and len(uid) > 0 :
            user_dn = __get_user_dn(uid)
            attrs.update( {MEMBER : [(MODIFY_DELETE, user_dn)]} )
            conn = ldaphelper.open()        
            id = conn.modify(__get_dn(entity), attrs)
    except Exception as e:
        raise LdapException('Remove member error=' + str(e), global_ids.ROLE_USER_DEASSIGN_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NO_SUCH_ATTRIBUTE:
            raise LdapException('Remove member failed, not assigned, role=' +  entity.name + ', member dn=' + user_dn)             
        elif result != 0:
            raise LdapException('Remove member failed result=' + str(result), global_ids.ROLE_USER_DEASSIGN_FAILED)                    
    return entity


def get_members (entity):
    __validate(entity, "Get Members")
    conn = None            
    uList = []
    search_filter = '(&(objectClass=' + ROLE_OC_NAME + ')'
    search_filter += '(' + ROLE_NAME + '=' + entity.name + '))'
    try:
        conn = ldaphelper.open()
        id = conn.search(search_base, search_filter, attributes=[MEMBER])
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)
    except Exception as e:
        raise LdapException('Get members search error=' + str(e))
    else:
        if total_entries == 0:
            raise NotFound("Role not found, name=" + entity.name)    
        elif total_entries > 1:
            raise NotUnique("Role not unique, name=" + entity.name)        
        member_dns = ldaphelper.get_list(response[0][ATTRIBUTES][MEMBER])
        uList = __convert_list(member_dns)
    finally:
        if conn:        
            ldaphelper.close(conn)
    return uList


def __validate(entity, op):
    if entity.name is None or len(entity.name) == 0 :
        __raise_exception(op, ROLE_NAME)

                    
def __raise_exception(operation, field):
    raise LdapException('roledao.' + operation + ' required field missing:' + field)


def __get_dn(entity):
    return global_ids.CN + '=' + entity.name + "," + search_base


def __get_user_dn(uid):
    # TODO: find a better way to do this:
    return global_ids.UID + '=' + uid + ',' + userdao.search_base


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
    global_ids.INTERNAL_ID, ROLE_NAME, global_ids.CONSTRAINT, global_ids.PROPS, global_ids.DESC
     ]

search_base = Config.get('dit')['roles']
ATTRIBUTES = 'attributes'