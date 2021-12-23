'''
@copyright: 2022 - Symas Corporation
'''

import uuid
import ldap
from ldap import MOD_REPLACE, MOD_ADD, MOD_DELETE
from ldap.cidict import cidict as CIDict
from rbac.model import User, Constraint
from rbac.ldap import ldaphelper, NotFound, NotUnique, InvalidCredentials
from rbac.ldap.ldaphelper import add_to_modlist, mods_to_modlist
from rbac.util import global_ids
from rbac.util.fortress_error import RbacError

def read (entity):
    userList = search(entity)
    if userList is None or len(userList) == 0:
        raise NotFound(msg="User Read not found, uid=" + entity.uid, id=global_ids.USER_NOT_FOUND)
    elif len(userList) > 1:
        raise NotUnique(msg="User Read not unique, uid=" + entity.uid, id=global_ids.USER_READ_FAILED)
    else:
        return userList[0]


def authenticate (entity):
    conn = None
    result = False            
    try:        
        conn = ldaphelper.open_user(__get_dn(entity), entity.password)
        # result = conn.bind() # TODO: WTH?
    except Exception as e:
        raise RbacError(msg='User Authenticate error for uid=' + entity.uid + ', LDAP error=' + str(e), id=global_ids.USER_PW_CHK_FAILED)
    finally:
        if conn:        
            ldaphelper.close_user(conn)
    return True


def search (entity):
    conn = None            
    userList = []
    search_filter = '(&(objectClass=' + USER_OC_NAME + ')'
    if entity.uid:
        search_filter += '(' + global_ids.UID + '=' + entity.uid + ')'
    if entity.ou:
        search_filter += '(' + global_ids.OU + '=' + entity.ou + ')'
    search_filter += ')'           
    try:
        conn = ldaphelper.open()
        entries = conn.search_s(CONTAINER_DN, scope=ldap.SCOPE_SUBTREE, filterstr=search_filter, attrlist=SEARCH_ATTRS)
        for dn, attrs in entries:
            userList.append(__unload(dn, attrs))
    except Exception as e:
        raise RbacError(msg='User Search error=' + str(e))
    finally:
        if conn:        
            ldaphelper.close(conn)
    return userList


# assumes that roles contains at least one role name
def search_on_roles (roles):    
    conn = None            
    userList = []    
    search_filter = '(&(objectClass=' + USER_OC_NAME + ')'
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
        entries = conn.search_s(CONTAINER_DN, scope=ldap.SCOPE_SUBTREE, filterstr=search_filter, attrlist=SEARCH_ATTRS)
        for dn, attrs in entries:
            userList.append(__unload(dn, attrs))
    except Exception as e:
        raise RbacError(msg='User Search Roles error=' + str(e), id=global_ids.URLE_SEARCH_FAILED)
    finally:
        if conn:        
            ldaphelper.close(conn)
    return userList


def __unload(dn, attrs):
    entity = User()
    entity.dn = dn

    attrs = CIDict(attrs)

    entity.uid = ldaphelper.get_one_attr_val(attrs.get(global_ids.UID, []))
    entity.ou = ldaphelper.get_one_attr_val(attrs.get(global_ids.OU, []))
    entity.internal_id = ldaphelper.get_attr_val(attrs.get(global_ids.INTERNAL_ID, []))
    entity.pw_policy = ldaphelper.get_attr_val(attrs.get(PW_POLICY, []))
    entity.cn = ldaphelper.get_one_attr_val(attrs.get(global_ids.CN, []))
    entity.sn = ldaphelper.get_one_attr_val(attrs.get(global_ids.SN, []))
    entity.description = ldaphelper.get_one_attr_val(attrs.get(global_ids.DESC, []))
    entity.display_name = ldaphelper.get_attr_val(attrs.get(DISPLAY_NAME, []))
    entity.employee_type = ldaphelper.get_one_attr_val(attrs.get(EMPLOYEE_TYPE, []))
    entity.title = ldaphelper.get_one_attr_val(attrs.get(TITLE, []))
    entity.reset = ldaphelper.get_bool(attrs.get(IS_RESET, []))
    entity.system = ldaphelper.get_bool(attrs.get(IS_SYSTEM, []))
    entity.department_number = ldaphelper.get_one_attr_val(attrs.get(DEPT_NUM, []))
    entity.l = ldaphelper.get_one_attr_val(attrs.get(LOCATION, []))
    entity.physical_delivery_office_name = ldaphelper.get_one_attr_val(attrs.get(PHYSICAL_OFFICE_NM, []))
    entity.postal_code = ldaphelper.get_one_attr_val(attrs.get(POSTAL_CODE, []))
    entity.room_number = ldaphelper.get_one_attr_val(attrs.get(RM_NUM, []))

    # Get the attr as object:
    entity.locked_time = ldaphelper.get_attr_object(attrs.get(LOCKED_TIME, []))

    # Get the multi-occurring attrs:
    entity.props = ldaphelper.get_list(attrs.get(global_ids.PROPS, []))
    entity.phones = ldaphelper.get_list(attrs.get(TELEPHONE_NUMBER, []))
    entity.mobiles = ldaphelper.get_list(attrs.get(MOBILE, []))
    entity.emails = ldaphelper.get_list(attrs.get(MAIL, []))
    entity.roles = ldaphelper.get_list(attrs.get(ROLES, []))

    # unload raw user constraint:
    entity.constraint = Constraint(ldaphelper.get_attr_val(attrs.get(global_ids.CONSTRAINT, [])))

    # now, unload raw user-role constraints:
    rcsRaw = ldaphelper.get_list(attrs.get(ROLE_CONSTRAINTS, []))
    if rcsRaw is not None :
        entity.role_constraints = []
        for rcRaw in rcsRaw :
            entity.role_constraints.append(Constraint(rcRaw))
                        
    return entity


def create ( entity ):
    try:
        attrs = {}
        attrs.update( {'objectClass': USER_OCS} )
        attrs.update( {global_ids.UID : entity.uid} )
        # generate random id:
        entity.internal_id = str(uuid.uuid4())
        attrs.update( {global_ids.INTERNAL_ID : entity.internal_id} )        
        # cn is req'd for iNetOrgPerson, if caller did not set, use uid value
        if not entity.cn:
            entity.cn = entity.uid
        attrs.update( {global_ids.CN : entity.cn} )
        # likewise sn is req'd for iNetOrgPerson, if caller did not set, use uid value
        if not entity.sn:
            entity.sn = entity.uid
        attrs.update( {global_ids.SN : entity.sn} )  
        # strings:  
        if entity.password:                
            attrs.update( {PW : entity.password} )
        if entity.description:        
            attrs.update( {global_ids.DESC : entity.description} )
        if entity.ou :        
            attrs.update( {global_ids.OU : entity.ou} )
        if entity.display_name:        
            attrs.update( {DISPLAY_NAME : entity.display_name} )
        if entity.employee_type:        
            attrs.update( {EMPLOYEE_TYPE : entity.employee_type} )
        if entity.title:        
            attrs.update( {TITLE : entity.title} )
        if entity.department_number:        
            attrs.update( {DEPT_NUM : entity.department_number} )
        if entity.l:        
            attrs.update( {LOCATION : entity.l} )
        if entity.physical_delivery_office_name:        
            attrs.update( {PHYSICAL_OFFICE_NM : entity.physical_delivery_office_name} )
        if entity.postal_code:        
            attrs.update( {POSTAL_CODE : entity.postal_code} )
        if entity.room_number:        
            attrs.update( {RM_NUM : entity.room_number} )                        
        if entity.pw_policy:        
            attrs.update( {PW_POLICY : entity.pw_policy} )
        # boolean:
        if entity.system is not None :        
            attrs.update( {IS_SYSTEM : 'TRUE' if entity.system else 'FALSE'} )
        # list of strings:
        if entity.phones is not None and len(entity.phones) > 0 :        
            attrs.update( {TELEPHONE_NUMBER : entity.phones} )
        if entity.mobiles is not None and len(entity.mobiles) > 0 :        
            attrs.update( {MOBILE : entity.mobiles} )
        if entity.emails is not None and len(entity.emails) > 0 :        
            attrs.update( {MAIL : entity.emails} )            
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : entity.props} )
        # list of delimited strings:
        if entity.constraint:        
            attrs.update( {global_ids.CONSTRAINT : entity.constraint.get_raw()} )
            
        conn = ldaphelper.open()     
        conn.add_s(__get_dn(entity), add_to_modlist(attrs))
    except ldap.ALREADY_EXISTS:
        raise NotUnique(msg='User create failed, already exists:' + entity.uid, id=global_ids.USER_ADD_FAILED)
    except ldap.LDAPError as e:
        raise RbacError(msg='User create failed result=' + str(e), id=global_ids.USER_ADD_FAILED)
    except Exception as e:
        raise RbacError(msg='User create error=' + str(e), id=global_ids.USER_ADD_FAILED)
    return entity


def update ( entity ):
    try:
        attrs = {}
        # strings:                
        if entity.cn:
            attrs.update( {global_ids.CN : [(MOD_REPLACE, [entity.cn])]} )
        if entity.sn:
            attrs.update( {global_ids.SN : [(MOD_REPLACE, [entity.sn])]} )
        if entity.password:                
            attrs.update( {PW : [(MOD_REPLACE, [entity.password])]} )
        if entity.description:        
            attrs.update( {global_ids.DESC : [(MOD_REPLACE, [entity.description])]} )
        if entity.ou:        
            attrs.update( {global_ids.OU : [(MOD_REPLACE, [entity.ou])]} )
        if entity.display_name:        
            attrs.update( {DISPLAY_NAME : [(MOD_REPLACE, [entity.display_name])]} )
        if entity.employee_type:        
            attrs.update( {EMPLOYEE_TYPE : [(MOD_REPLACE, entity.employee_type)]} )
        if entity.title:        
            attrs.update( {TITLE : [(MOD_REPLACE, [entity.title])]} )
        if entity.department_number:        
            attrs.update( {DEPT_NUM : [(MOD_REPLACE, entity.department_number)]} )
        if entity.l:        
            attrs.update( {LOCATION : [(MOD_REPLACE, entity.l)]} )
        if entity.physical_delivery_office_name:        
            attrs.update( {PHYSICAL_OFFICE_NM : [(MOD_REPLACE, entity.physical_delivery_office_name)]} )
        if entity.postal_code:        
            attrs.update( {POSTAL_CODE : [(MOD_REPLACE, entity.postal_code)]} )
        if entity.room_number:        
            attrs.update( {RM_NUM : [(MOD_REPLACE, entity.room_number)]} )
        if entity.pw_policy:        
            attrs.update( {PW_POLICY : [(MOD_REPLACE, entity.pw_policy)]} )
            
        # list of strings:
        if entity.phones is not None and len(entity.phones) > 0 :        
            attrs.update( {TELEPHONE_NUMBER : [(MOD_REPLACE, entity.phones)]} )
        if entity.mobiles is not None and len(entity.mobiles) > 0 :        
            attrs.update( {MOBILE : [(MOD_REPLACE, entity.mobiles)]} )
        if entity.emails is not None and len(entity.emails) > 0 :        
            attrs.update( {MAIL : [(MOD_REPLACE, entity.emails)]} )
        if entity.system is not None :        
            attrs.update( {IS_SYSTEM : [(MOD_REPLACE, 'TRUE' if entity.system else 'FALSE')]} )

        # list of delimited strings::
        if entity.constraint is not None :        
            attrs.update( {global_ids.CONSTRAINT : [(MOD_REPLACE, entity.constraint.get_raw())]} )
            
        # boolean:
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : [(MOD_REPLACE, entity.props)]} )
            
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            conn.modify_s(__get_dn(entity), mods_to_modlist(attrs))
    except ldap.NO_SUCH_OBJECT:
        raise NotFound(msg='User update failed, not found:' + entity.name, id=global_ids.USER_UPDATE_FAILED)
    except ldap.LDAPError as e:
        raise RbacError(msg='User update failed result=' + str(e), id=global_ids.USER_UPDATE_FAILED)
    except Exception as e:
        raise RbacError(msg='User update error=' + str(e), id=global_ids.USER_UPDATE_FAILED)
    return entity


def delete ( entity ):
    try:
        conn = ldaphelper.open()        
        conn.delete_s(__get_dn(entity))
    except ldap.NO_SUCH_OBJECT:
        raise RbacError(msg='User delete not found:' + entity.uid, id=global_ids.USER_NOT_FOUND)
    except ldap.LDAPError as e:
        raise RbacError(msg='User delete failed result=' + str(e), id=global_ids.USER_DELETE_FAILED)
    except Exception as e:
        raise RbacError(msg='User delete error=' + str(e), id=global_ids.USER_DELETE_FAILED)
    return entity


def assign ( entity, constraint ):
    try:
        attrs = {}
        if constraint is not None:
            attrs.update( {ROLE_CONSTRAINTS : [(MOD_ADD, constraint.get_raw())]} )
            attrs.update( {ROLES : [(MOD_ADD, constraint.name)]} )
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            conn.modify_s(__get_dn(entity), mods_to_modlist(attrs))
    except ldap.NO_SUCH_OBJECT:
        raise RbacError(msg='User assign failed, not found:' + entity.uid, id=global_ids.USER_NOT_FOUND)
    except ldap.LDAPError as e:
        raise RbacError(msg='User assign failed result=' + str(e), id=global_ids.URLE_ASSIGN_FAILED)
    except Exception as e:
        raise RbacError(msg='User assign error=' + str(e), id=global_ids.URLE_ASSIGN_FAILED)
    return entity


def deassign ( entity, constraint ):
    try:
        attrs = {}
        if constraint is not None:
            attrs.update( {ROLE_CONSTRAINTS : [(MOD_DELETE, constraint.get_raw())]} )
            attrs.update( {ROLES : [(MOD_DELETE, constraint.name)]} )
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            conn.modify_s(__get_dn(entity), mods_to_modlist(attrs))
    except ldap.NO_SUCH_OBJECT:
        raise RbacError(msg='User deassign failed, not found:' + entity.uid, id=global_ids.USER_NOT_FOUND)
    except ldap.NO_SUCH_ATTRIBUTE:
        raise RbacError(msg='User deassign failed, no such attribute=' + constraint.name, id=global_ids.URLE_ASSIGN_NOT_EXIST)
    except ldap.LDAPError as e:
        raise RbacError(msg='User deassign failed result=' + str(e), id=global_ids.URLE_ASSIGN_FAILED)
    except Exception as e:
        raise RbacError(msg='User deassign error=' + str(e), id=global_ids.URLE_DEASSIGN_FAILED)
    return entity


def __get_dn(entity):
    return global_ids.UID + '=' + entity.uid + ',' + CONTAINER_DN


USER_OC_NAME = 'inetOrgPerson'
USER_ATTRS_OC_NAME = 'ftUserAttrs'
USER_OCS = [USER_OC_NAME, USER_ATTRS_OC_NAME, global_ids.PROP_OC_NAME]

PW = 'userPassword'
ROLES = 'ftra'
PW_POLICY = 'pwdPolicySubentry'
ROLE_CONSTRAINTS = 'ftRC'
DISPLAY_NAME = 'displayName'
EMPLOYEE_TYPE = 'employeeType'
TITLE = 'title'
TELEPHONE_NUMBER = 'telephoneNumber'
MOBILE = 'mobile'
MAIL = 'mail'
IS_RESET = 'pwdReset'
LOCKED_TIME = 'pwdAccountLockedTime'
IS_SYSTEM = 'ftSystem'
DEPT_NUM = 'departmentNumber'
LOCATION = 'l'
PHYSICAL_OFFICE_NM = 'physicalDeliveryOfficeName'
POSTAL_CODE = 'postalCode'
RM_NUM = 'roomNumber'

SEARCH_ATTRS = [
    global_ids.UID, global_ids.OU, global_ids.INTERNAL_ID, ROLES, ROLE_CONSTRAINTS, PW_POLICY, global_ids.CONSTRAINT,
    global_ids.CN, global_ids.SN, global_ids.DESC, DISPLAY_NAME, EMPLOYEE_TYPE,
    TITLE, TELEPHONE_NUMBER, MOBILE, MAIL, IS_RESET,
    LOCKED_TIME, IS_SYSTEM, global_ids.PROPS, DEPT_NUM,
    PHYSICAL_OFFICE_NM, POSTAL_CODE, RM_NUM, LOCATION
    ]

CONTAINER_DN = ldaphelper.get_container_dn(global_ids.USER_OU)
