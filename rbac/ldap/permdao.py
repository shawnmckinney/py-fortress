'''
@copyright: 2022 - Symas Corporation
'''

import uuid    
import ldap
from ldap import MOD_REPLACE, MOD_ADD, MOD_DELETE
from ldap.cidict import cidict as CIDict
from rbac.model import Perm, PermObj
from rbac.ldap import ldaphelper, NotFound, NotUnique
from rbac.ldap.ldaphelper import add_to_modlist
from rbac.util import global_ids
from rbac.util.fortress_error import RbacError


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
        entries = conn.search_s(__CONTAINER_DN, scope=ldap.SCOPE_SUBTREE, filterstr=search_filter, attrlist=SEARCH_ATTRS)
        for dn, attrs in entries:
            permList.append(__unload(dn, attrs))
    except Exception as e:
        raise RbacError(msg='Perm search error=' + str(e), id=global_ids.PERM_SEARCH_FAILED)
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
        entries = conn.search_s(__CONTAINER_DN, scope=ldap.SCOPE_SUBTREE, filterstr=search_filter, attrlist=SEARCH_ATTRS)
        for dn, attrs in entries:
            permList.append(__unload_obj(dn, attrs))
    except Exception as e:
        raise RbacError(msg='PermObj search error=' + str(e), id=global_ids.PERM_SEARCH_FAILED)
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
        entries = conn.search_s(__CONTAINER_DN, scope=ldap.SCOPE_SUBTREE, filterstr=search_filter, attrlist=SEARCH_ATTRS)
        for dn, attrs in entries:
            permList.append(__unload(dn, attrs))
    except Exception as e:
        raise RbacError(msg='Perm Search Roles error=' + str(e), id=global_ids.PERM_ROLE_SEARCH_FAILED)
    finally:
        if conn:        
            ldaphelper.close(conn)
    return permList


def __unload(dn, attrs):
    entity = Perm()
    entity.dn = dn

    attrs = CIDict(attrs)

    entity.internal_id = ldaphelper.get_attr_val(attrs.get(global_ids.INTERNAL_ID, []))
    entity.obj_id = ldaphelper.get_attr_val(attrs.get(OBJ_ID, []))
    entity.obj_name = ldaphelper.get_attr_val(attrs.get(OBJ_NM, []))
    entity.op_name = ldaphelper.get_attr_val(attrs.get(OP_NM, []))
    entity.abstract_name = ldaphelper.get_attr_val(attrs.get(PERM_NAME, []))
    entity.type = ldaphelper.get_attr_val(attrs.get(TYPE, []))
    entity.description = ldaphelper.get_one_attr_val(attrs.get(global_ids.DESC, []))
    # Get the multi-occurring attrs:
    entity.users = ldaphelper.get_list(attrs.get(USERS, []))
    entity.roles = ldaphelper.get_list(attrs.get(ROLES, []))
    entity.props = ldaphelper.get_list(attrs.get(global_ids.PROPS, []))
    return entity


def __unload_obj(dn, attrs):
    entity = PermObj()

    attrs = CIDict(attrs)

    entity.dn = dn
    entity.internal_id = ldaphelper.get_attr_val(attrs.get(global_ids.INTERNAL_ID, []))
    entity.obj_name = ldaphelper.get_attr_val(attrs.get(OBJ_NM, []))
    entity.type = ldaphelper.get_attr_val(attrs.get(TYPE, []))
    entity.description = ldaphelper.get_one_attr_val(attrs.get(global_ids.DESC, []))
    entity.ou = ldaphelper.get_one_attr_val(attrs.get(global_ids.OU, []))
    entity.props = ldaphelper.get_list(attrs.get(global_ids.PROPS, []))
    return entity


def create ( entity ):
    try:
        attrs = {}
        attrs.update( {'objectClass': PERM_OCS} )
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
        conn.add_s(__get_dn(entity), add_to_modlist(attrs))
    except ldap.ALREADY_EXISTS:
        raise NotUnique(msg='Perm create failed, already exists:' + entity.obj_name, id=global_ids.PERM_ADD_FAILED)
    except ldap.LDAPError as e:
        raise RbacError(msg='Perm create failed result=' + str(e), id=global_ids.PERM_ADD_FAILED)
    except Exception as e:
        raise RbacError(msg='Perm create error=' + str(e), id=global_ids.PERM_ADD_FAILED)
    return entity


def update ( entity ):
    try:
        attrs = {}
        if entity.description:        
            attrs.update( {global_ids.DESC : [(MOD_REPLACE, [entity.description])]} )
        if entity.type:        
            attrs.update( {TYPE : [(MOD_REPLACE, [entity.type])]} )
        # list of strings:
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : [(MOD_REPLACE, entity.props)]} )
        if entity.users is not None and len(entity.users) > 0 :        
            attrs.update( {USERS : [(MOD_REPLACE, entity.users)]} )
        if entity.roles is not None and len(entity.roles) > 0 :        
            attrs.update( {ROLES : [(MOD_REPLACE, entity.roles)]} )
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            conn.modify_s(__get_dn(entity), attrs_to_modlist(attrs))
    except ldap.NO_SUCH_OBJECT:
        raise NotFound(msg='Perm update failed, not found:' + entity.obj_name, id=global_ids.PERM_OP_NOT_FOUND)
    except ldap.LDAPError as e:
        raise RbacError(msg='Perm update failed result=' + str(e), id=global_ids.PERM_UPDATE_FAILED)
    except Exception as e:
        raise RbacError(msg='Perm update error=' + str(e), id=global_ids.PERM_UPDATE_FAILED)
    return entity


def delete ( entity ):
    try:
        conn = ldaphelper.open()        
        conn.delete_s(__get_dn(entity))
    except ldap.NO_SUCH_OBJECT:
        raise NotFound(msg='Perm delete not found:' + entity.obj_name, id=global_ids.PERM_OP_NOT_FOUND)
    except ldap.LDAPError as e:
        raise RbacError(msg='Perm delete failed result=' + str(e), id=global_ids.PERM_DELETE_FAILED)
    except Exception as e:
        raise RbacError(msg='Perm delete error=' + str(e), id=global_ids.PERM_DELETE_FAILED)
    return entity


def grant ( entity, role ):
    try:
        attrs = {}
        # constraint type:
        if role is not None:
            attrs.update( {ROLES : [(MOD_ADD, role.name)]} )
            conn = ldaphelper.open()
            conn.modify_s(__get_dn(entity), attrs_to_modlist(attrs))
    except ldap.NO_SUCH_OBJECT:
        raise NotFound(msg='Perm grant failed, not found, obj name='
                            +  entity.obj_name + ', op_name='
                            + entity.op_name
                            + ', op id=' + entity.obj_id
                            + ', role='+ role.name,
                            id=global_ids.PERM_OP_NOT_FOUND)
    except ldap.LDAPError as e:
        raise RbacError(msg='Perm grant failed result=' + str(e), id=global_ids.PERM_GRANT_FAILED)
    except Exception as e:
        raise RbacError(msg='Perm grant error=' + str(e), id=global_ids.PERM_GRANT_FAILED)
    return entity


def revoke ( entity, role ):
    try:
        attrs = {}
        # constraint type:
        if role is not None:
            attrs.update( {ROLES : [(MOD_DELETE, role.name)]} )
            conn = ldaphelper.open()
            conn.modify_s(__get_dn(entity), attrs_to_modlist(attrs))
    except ldap.NO_SUCH_OBJECT:
        raise FortressError(msg='Perm not found, obj name='
                            +  entity.obj_name
                            + ', op_name='
                            + entity.op_name
                            + ', role='
                            + role.name,
                            id=global_ids.PERM_NOT_EXIST)
    except ldap.NO_SUCH_ATTRIBUTE:
        raise FortressError(msg='Perm revoke failed, not granted, obj name='
                            +  entity.obj_name
                            + ', op_name='
                            + entity.op_name
                            + ', role='
                            + role.name,
                            id=global_ids.PERM_ROLE_NOT_EXIST)
    except ldap.LDAPError as e:
        raise FortressError(msg='Perm revoke failed result=' + str(e), id=global_ids.PERM_REVOKE_FAILED)
    except Exception as e:
        raise FortressError(msg='Perm revoke error=' + str(e), id=global_ids.PERM_REVOKE_FAILED)
    return entity


def create_obj ( entity ):
    try:
        attrs = {}
        attrs.update( {'objectClass': PERM_OBJ_OCS} )
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
        conn.add_s(__get_obj_dn(entity), add_to_modlist(attrs))
    except ldap.ALREADY_EXISTS:
        raise NotUnique(msg='PermObj create failed, already exists:' + entity.uid, id=global_ids.PERM_ADD_FAILED)
    except ldap.LDAPError as e:
        raise FortressError(msg='PermObj create failed result=' + str(e), id=global_ids.PERM_ADD_FAILED)
    except Exception as e:
        raise FortressError(msg='PermObj create error=' + str(e), id=global_ids.PERM_ADD_FAILED)
    return entity


def update_obj ( entity ):
    conn = None
    try:
        attrs = {}        
        if entity.ou:        
            attrs.update( {global_ids.OU : [(MOD_REPLACE, [entity.ou])]} )
        if entity.description:        
            attrs.update( {global_ids.DESC : [(MOD_REPLACE, [entity.description])]} )
        if entity.type:        
            attrs.update( {TYPE : [(MOD_REPLACE, [entity.type])]} )
        # list of comma delimited strings:
        if entity.props is not None and len(entity.props) > 0 :
            attrs.update( {global_ids.PROPS : [(MOD_REPLACE, entity.props)]} )
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            conn.modify_s(__get_obj_dn(entity), attrs_to_modlist(attrs))
    except ldap.NO_SUCH_OBJECT:
        raise NotFound(msg='PermObj update failed, not found:' + entity.obj_name, id=global_ids.PERM_OBJ_NOT_FOUND)
    except ldap.LDAPError as e:
        raise FortressError(msg='PermObj update failed result=' + str(e), id=global_ids.PERM_UPDATE_FAILED)
    except Exception as e:
        raise FortressError(msg='PermObj update error=' + str(e), id=global_ids.PERM_UPDATE_FAILED)
    return entity


def delete_obj ( entity ):
    try:
        conn = ldaphelper.open()        
        conn.delete_s(__get_obj_dn(entity))
    except ldap.NO_SUCH_OBJECT:
        raise NotFound(msg='PermObj delete not found:' + entity.obj_name, id=global_ids.PERM_OBJ_NOT_FOUND)
    except ldap.LDAPError as e:
        raise FortressError(msg='PermObj delete failed result=' + str(e), id=global_ids.PERM_DELETE_FAILED)
    except Exception as e:
        raise FortressError(msg='PermObj delete error=' + str(e), id=global_ids.PERM_DELETE_FAILED)
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


def attrs_to_modlist(attrs):
    result = []
    for attr, mods in attrs.items():
        for op, vals in mods:
            if not isinstance(vals, (tuple, list)):
                vals = [vals]
            vals = [v.encode() if isinstance(v, str) else v for v in vals]
            result.append((op, attr, vals))
    return result


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
