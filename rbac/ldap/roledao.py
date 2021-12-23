'''
@copyright: 2022 - Symas Corporation
'''

import uuid
import ldap
from ldap import MOD_REPLACE, MOD_ADD, MOD_DELETE
from ldap.cidict import cidict as CIDict
from ldap.dn import str2dn
from rbac.model import Role, Constraint
from rbac.ldap import ldaphelper, NotFound, NotUnique
from rbac.ldap import userdao
from rbac.ldap.ldaphelper import add_to_modlist, mods_to_modlist
from rbac.util import global_ids
from rbac.util.fortress_error import RbacError

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
        entries = conn.search_s(__CONTAINER_DN, scope=ldap.SCOPE_SUBTREE, filterstr=search_filter, attrlist=SEARCH_ATTRS)
        for dn, attrs in entries:
            roleList.append(__unload(dn, attrs))
    except Exception as e:
        raise RbacError(msg='Role search error=' + str(e), id=global_ids.ROLE_SEARCH_FAILED)
    finally:
        if conn:        
            ldaphelper.close(conn)
    return roleList


def __unload(dn, attrs):
    entity = Role()
    entity.dn = dn

    attrs = CIDict(attrs)

    entity.internal_id = ldaphelper.get_attr_val(attrs.get(global_ids.INTERNAL_ID, []))
    entity.name = ldaphelper.get_attr_val(attrs.get(ROLE_NAME, []))
    entity.description = ldaphelper.get_one_attr_val(attrs.get(global_ids.DESC, []))
    # Get the multi-occurring attrs:
    entity.props = ldaphelper.get_list(attrs.get(global_ids.PROPS, []))
    entity.members = ldaphelper.get_list(attrs.get(MEMBER, []))
    # unload raw constraint:
    entity.constraint = Constraint(ldaphelper.get_attr_val(attrs.get(global_ids.CONSTRAINT, [])))
    return entity


def create ( entity ):
    try:
        attrs = {}
        attrs.update( {'objectClass': ROLE_OCS} )
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
        conn.add_s(__get_dn(entity), add_to_modlist(attrs))
    except ldap.ALREADY_EXISTS:
        raise NotUnique(msg='Role create failed, already exists:' + entity.uid, id=global_ids.ROLE_ADD_FAILED)
    except ldap.LDAPError as e:
        raise RbacError(msg='Role create failed result=' + str(e), id=global_ids.ROLE_ADD_FAILED)
    except Exception as e:
        raise RbacError(msg='Role create error=' + str(e), id=global_ids.ROLE_ADD_FAILED)
    return entity


def update ( entity ):
    try:
        attrs = {}
        if entity.description:        
            attrs.update( {global_ids.DESC : [(MOD_REPLACE, [entity.description])]} )
        # list of srings:
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : [(MOD_REPLACE, [entity.props])]} )
        # list of comma delimited strings:
        if entity.constraint is not None :        
            attrs.update( {global_ids.CONSTRAINT : [(MOD_REPLACE, [entity.constraint.get_raw()])]} )
        if len(attrs) > 0:
            conn = ldaphelper.open()        
            conn.modify_s(__get_dn(entity), mods_to_modlist(attrs))
    except ldap.NO_SUCH_OBJECT:
        raise NotFound(msg='Role update failed, not found:' + entity.name, id=global_ids.ROLE_NOT_FOUND)
    except ldap.LDAPError as e:
        raise RbacError('Role update failed result=' + str(e), global_ids.ROLE_UPDATE_FAILED)
    except Exception as e:
        raise RbacError(msg='Role update error=' + str(e), id=global_ids.ROLE_UPDATE_FAILED)
    return entity


def delete ( entity ):
    try:
        conn = ldaphelper.open()        
        conn.delete_s(__get_dn(entity))
    except ldap.NO_SUCH_OBJECT:
        raise NotFound(msg='Role delete not found:' + entity.name, id=global_ids.ROLE_NOT_FOUND)
    except ldap.LDAPError as e:
        raise RbacError(msg='Role delete failed result=' + str(e), id=global_ids.ROLE_DELETE_FAILED)
    except Exception as e:
        raise RbacError(msg='Role delete error=' + str(e), id=global_ids.ROLE_DELETE_FAILED)
    return entity


def add_member ( entity, uid ):    
    try:        
        attrs = {}
        if uid:
            user_dn = __get_user_dn(uid)            
            attrs.update( {MEMBER : [(MOD_ADD, user_dn)]} )
            conn = ldaphelper.open()
            conn.modify_s(__get_dn(entity), mods_to_modlist(attrs))
    except ldap.NO_SUCH_OBJECT:
        raise NotFound(msg='Add member failed, not found, role=' +  entity.name + ', member dn=' + user_dn, id=global_ids.ROLE_NOT_FOUND)
    except ldap.LDAPError as e:
        raise RbacError(msg='Add member failed result=' + str(e), id=global_ids.ROLE_USER_ASSIGN_FAILED)
    except Exception as e:
        raise RbacError(msg='Add member error=' + str(e), id=global_ids.ROLE_USER_ASSIGN_FAILED)
    return entity


def remove_member ( entity, uid ):    
    try:        
        attrs = {}
        if uid:
            user_dn = __get_user_dn(uid)
            attrs.update( {MEMBER : [(MOD_DELETE, user_dn)]} )
            conn = ldaphelper.open()
            conn.modify_s(__get_dn(entity), mods_to_modlist(attrs))
    except ldap.NO_SUCH_ATTRIBUTE:
        raise RbacError(msg='Remove member failed, not assigned, role=' +  entity.name + ', member dn=' + user_dn, id=global_ids.URLE_ASSIGN_NOT_EXIST)
    except ldap.LDAPError as e:
        raise RbacError(msg='Remove member failed result=' + str(e), id=global_ids.ROLE_REMOVE_OCCUPANT_FAILED)
    except Exception as e:
        raise RbacError(msg='Remove member error=' + str(e), id=global_ids.ROLE_REMOVE_OCCUPANT_FAILED)
    return entity


def get_members (entity):
    conn = None            
    uList = []
    search_filter = '(&(objectClass=' + ROLE_OC_NAME + ')'
    search_filter += '(' + ROLE_NAME + '=' + entity.name + '))'
    try:
        conn = ldaphelper.open()
        # TODO: use sizelimit=1
        entries = conn.search_s(__CONTAINER_DN, scope=ldap.SCOPE_SUBTREE, filterstr=search_filter, attrlist=SEARCH_ATTRS)

        if not entries:
            raise NotFound(msg="Role not found, name=" + entity.name, id=global_ids.ROLE_NOT_FOUND)
        elif len(entries) > 1:
            raise NotUnique(msg="Role not unique, name=" + entity.name, id=global_ids.ROLE_SEARCH_FAILED)

        dn, attrs = entries[0]

        member_dns = ldaphelper.get_list(attrs.get(MEMBER, []))
        uList = __convert_list(member_dns)
    except Exception as e: # FIXME: change to LDAPError
        raise RbacError(msg='Get members search error=' + str(e), id=global_ids.ROLE_OCCUPANT_SEARCH_FAILED)
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
        # TODO: use sizelimit=1
        entries = conn.search_s(__CONTAINER_DN, scope=ldap.SCOPE_SUBTREE, filterstr=search_filter, attrlist=[MEMBER, global_ids.CONSTRAINT])

        if not entries:
            raise NotFound(msg="Role not found, name=" + entity.name, id=global_ids.ROLE_NOT_FOUND)
        elif len(entries) > 1:
            raise NotUnique(msg="Role not unique, name=" + entity.name, id=global_ids.ROLE_SEARCH_FAILED)

        dn, attrs = entries[0]

        member_dns = ldaphelper.get_list(attrs.get(MEMBER, []))
        constraint = Constraint(ldaphelper.get_attr_val(attrs.get(global_ids.CONSTRAINT, [])))
        mList = __convert_list(member_dns)
    except Exception as e: # FIXME: change to LDAPError
        raise RbacError(msg='Get members search error=' + str(e), id=global_ids.ROLE_OCCUPANT_SEARCH_FAILED)
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
    return [__get_user_id(dn) for dn in list_dns]


def __get_user_id(user_dn):
    dn = str2dn(user_dn)
    for attr, value, _ in dn[0]:
        if attr.lower() == "uid":
            return value
    

ROLE_OC_NAME = 'ftRls'
ROLE_OCS = [ROLE_OC_NAME, global_ids.PROP_OC_NAME]
ROLE_NAME = 'ftRoleName'
MEMBER = 'roleOccupant'

SEARCH_ATTRS = [
    global_ids.INTERNAL_ID, ROLE_NAME, global_ids.CONSTRAINT, global_ids.PROPS, global_ids.DESC, MEMBER
     ]

__CONTAINER_DN = ldaphelper.get_container_dn(global_ids.ROLE_OU)
