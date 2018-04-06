'''
Created on Feb 10, 2018

@author: smckinney
@copyright: 2018 - Symas Corporation
'''
    
import uuid
from ldap3 import MODIFY_REPLACE, MODIFY_ADD, MODIFY_DELETE    
from ..model import User, Constraint
from ..ldap import ldaphelper, NotFound, NotUnique, InvalidCredentials
from ..util import global_ids
from ..util import FortressError


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
        result = conn.bind()
    except Exception as e:
        raise FortressError(msg='User Authenticate error for uid=' + entity.uid + ', LDAP error=' + str(e), id=global_ids.USER_PW_CHK_FAILED)
    finally:
        if conn:        
            ldaphelper.close_user(conn)
    if result is False:
        raise InvalidCredentials(msg="User Authenticate invalid creds, uid=" + entity.uid, id=global_ids.USER_PW_INVLD)        
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
        id = conn.search(CONTAINER_DN, search_filter, attributes=SEARCH_ATTRS)
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)        
    except Exception as e:
        raise FortressError(msg='User Search error=' + str(e))    
    else:        
        if total_entries > 0:
            for entry in response:
                userList.append(__unload(entry))
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
        id = conn.search(CONTAINER_DN, search_filter, attributes=SEARCH_ATTRS)
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)        
    except Exception as e:
        raise FortressError(msg='User Search Roles error=' + str(e), id=global_ids.URLE_SEARCH_FAILED)
    else:        
        if total_entries > 0:
            for entry in response:
                userList.append(__unload(entry))
    finally:
        if conn:        
            ldaphelper.close(conn)
    return userList


def __unload(entry):
    entity = User()
    entity.dn = ldaphelper.get_dn(entry)        
    entity.uid = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][global_ids.UID])
    entity.ou = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][global_ids.OU])  
    entity.internal_id = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][global_ids.INTERNAL_ID])    
    entity.pw_policy = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][PW_POLICY])
    entity.cn = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][global_ids.CN])
    entity.sn = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][global_ids.SN])
    entity.description = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][global_ids.DESC])
    entity.display_name = ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][DISPLAY_NAME])
    entity.employee_type = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][EMPLOYEE_TYPE])
    entity.title = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][TITLE])
    entity.reset = ldaphelper.get_bool(entry[global_ids.ATTRIBUTES][IS_RESET])
    entity.system = ldaphelper.get_bool(entry[global_ids.ATTRIBUTES][IS_SYSTEM])
    entity.department_number = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][DEPT_NUM])
    entity.l = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][LOCATION])
    entity.physical_delivery_office_name = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][PHYSICAL_OFFICE_NM])
    entity.postal_code = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][POSTAL_CODE])
    entity.room_number = ldaphelper.get_one_attr_val(entry[global_ids.ATTRIBUTES][RM_NUM])

    # Get the attr as object:
    entity.locked_time = ldaphelper.get_attr_object(entry[global_ids.ATTRIBUTES][LOCKED_TIME])

    # Get the multi-occurring attrs:
    entity.props = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][global_ids.PROPS])    
    entity.phones = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][TELEPHONE_NUMBER])
    entity.mobiles = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][MOBILE])
    entity.emails = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][MAIL])
    entity.roles = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][ROLES])
    
    # unload raw user constraint:
    entity.constraint = Constraint(ldaphelper.get_attr_val(entry[global_ids.ATTRIBUTES][global_ids.CONSTRAINT]))
    
    # now, unload raw user-role constraints:    
    rcsRaw = ldaphelper.get_list(entry[global_ids.ATTRIBUTES][ROLE_CONSTRAINTS])
    if rcsRaw is not None :
        entity.role_constraints = []
        for rcRaw in rcsRaw :
            entity.role_constraints.append(Constraint(rcRaw))
                        
    return entity


def create ( entity ):
    try:
        attrs = {}
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
            attrs.update( {IS_SYSTEM : entity.system} )
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
        id = conn.add(__get_dn(entity), USER_OCS, attrs)
    except Exception as e:
        raise FortressError(msg='User create error=' + str(e), id=global_ids.USER_ADD_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.OBJECT_ALREADY_EXISTS:
            raise NotUnique(msg='User create failed, already exists:' + entity.uid, id=global_ids.USER_ADD_FAILED)             
        elif result != 0:
            raise FortressError(msg='User create failed result=' + str(result), id=global_ids.USER_ADD_FAILED)                    
    return entity


def update ( entity ):
    try:
        attrs = {}
        # strings:                
        if entity.cn:
            attrs.update( {global_ids.CN : [(MODIFY_REPLACE, [entity.cn])]} )
        if entity.sn:
            attrs.update( {global_ids.SN : [(MODIFY_REPLACE, [entity.sn])]} )
        if entity.password:                
            attrs.update( {PW : [(MODIFY_REPLACE, [entity.password])]} )
        if entity.description:        
            attrs.update( {global_ids.DESC : [(MODIFY_REPLACE, [entity.description])]} )
        if entity.ou:        
            attrs.update( {global_ids.OU : [(MODIFY_REPLACE, [entity.ou])]} )
        if entity.display_name:        
            attrs.update( {DISPLAY_NAME : [(MODIFY_REPLACE, [entity.display_name])]} )
        if entity.employee_type:        
            attrs.update( {EMPLOYEE_TYPE : [(MODIFY_REPLACE, entity.employee_type)]} )
        if entity.title:        
            attrs.update( {TITLE : [(MODIFY_REPLACE, [entity.title])]} )
        if entity.department_number:        
            attrs.update( {DEPT_NUM : [(MODIFY_REPLACE, entity.department_number)]} )
        if entity.l:        
            attrs.update( {LOCATION : [(MODIFY_REPLACE, entity.l)]} )
        if entity.physical_delivery_office_name:        
            attrs.update( {PHYSICAL_OFFICE_NM : [(MODIFY_REPLACE, entity.physical_delivery_office_name)]} )
        if entity.postal_code:        
            attrs.update( {POSTAL_CODE : [(MODIFY_REPLACE, entity.postal_code)]} )
        if entity.room_number:        
            attrs.update( {RM_NUM : [(MODIFY_REPLACE, entity.room_number)]} )      
        if entity.pw_policy:        
            attrs.update( {PW_POLICY : [(MODIFY_REPLACE, entity.pw_policy)]} )
            
        # list of strings:
        if entity.phones is not None and len(entity.phones) > 0 :        
            attrs.update( {TELEPHONE_NUMBER : [(MODIFY_REPLACE, entity.phones)]} )           
        if entity.mobiles is not None and len(entity.mobiles) > 0 :        
            attrs.update( {MOBILE : [(MODIFY_REPLACE, entity.mobiles)]} )
        if entity.emails is not None and len(entity.emails) > 0 :        
            attrs.update( {MAIL : [(MODIFY_REPLACE, entity.emails)]} )
        if entity.system is not None :        
            attrs.update( {IS_SYSTEM : [(MODIFY_REPLACE, entity.system)]} )

        # list of delimited strings::
        if entity.constraint is not None :        
            attrs.update( {global_ids.CONSTRAINT : [(MODIFY_REPLACE, entity.constraint.get_raw())]} )
            
        # boolean:
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : [(MODIFY_REPLACE, entity.props)]} )
            
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            id = conn.modify(__get_dn(entity), attrs)
    except Exception as e:
        raise FortressError(msg='User update error=' + str(e), id=global_ids.USER_UPDATE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='User update failed, not found:' + entity.name, id=global_ids.USER_UPDATE_FAILED)             
        elif result != 0:
            raise FortressError(msg='User update failed result=' + str(result), id=global_ids.USER_UPDATE_FAILED)                    
    return entity


def delete ( entity ):
    try:
        conn = ldaphelper.open()        
        id = conn.delete(__get_dn(entity))
    except Exception as e:
        raise FortressError(msg='User delete error=' + str(e), id=global_ids.USER_DELETE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise FortressError(msg='User delete not found:' + entity.uid, id=global_ids.USER_NOT_FOUND)                    
        elif result != 0:
            raise FortressError(msg='User delete failed result=' + str(result), id=global_ids.USER_DELETE_FAILED)                    
    return entity


def assign ( entity, constraint ):
    try:
        attrs = {}
        if constraint is not None:
            attrs.update( {ROLE_CONSTRAINTS : [(MODIFY_ADD, constraint.get_raw())]} )
            attrs.update( {ROLES : [(MODIFY_ADD, constraint.name)]} )                                     
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            id = conn.modify(__get_dn(entity), attrs)
    except Exception as e:
        raise FortressError(msg='User assign error=' + str(e), id=global_ids.URLE_ASSIGN_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='User assign failed, not found:' + entity.uid, id=global_ids.USER_NOT_FOUND)             
        elif result != 0:
            raise FortressError(msg='User assign failed result=' + str(result), id=global_ids.URLE_ASSIGN_FAILED)                    
    return entity


def deassign ( entity, constraint ):
    try:
        attrs = {}
        if constraint is not None:
            attrs.update( {ROLE_CONSTRAINTS : [(MODIFY_DELETE, constraint.get_raw())]} )
            attrs.update( {ROLES : [(MODIFY_DELETE, constraint.name)]} )                                     
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            id = conn.modify(__get_dn(entity), attrs)
    except Exception as e:
        raise FortressError(msg='User deassign error=' + str(e), id=global_ids.URLE_DEASSIGN_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='User deassign failed, not found:' + entity.uid, id=global_ids.USER_NOT_FOUND)
        elif result == global_ids.NO_SUCH_ATTRIBUTE:
            raise FortressError(msg='User deassign failed, no such attribute=' + constraint.name, id=global_ids.URLE_ASSIGN_NOT_EXIST)                     
        elif result != 0:
            raise FortressError(msg='User deassign failed result=' + str(result), id=global_ids.URLE_DEASSIGN_FAILED)                    
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