'''
Created on Feb 10, 2018

@author: smckinney
@copyright: 2018 - Symas Corporation
'''
    
import uuid    
from model import User, Constraint
from ldap import ldaphelper, LdapException, NotFound, NotUnique, InvalidCredentials
from ldap3 import MODIFY_REPLACE, MODIFY_ADD, MODIFY_DELETE
from util import Config, global_ids


def read (entity):
    userList = search(entity)
    if userList is None or len(userList) == 0:
        raise NotFound("User Read not found, uid=" + entity.uid)
    elif len(userList) > 1:
        raise NotUnique("User Read not unique, uid=" + entity.uid)
    else:
        return userList[0]


def authenticate (entity):
    __validate(entity, "User Bind")
    conn = None
    result = False            
    try:        
        conn = ldaphelper.open_user(__get_dn(entity), entity.password)
        result = conn.bind()
    except Exception as e:
        raise LdapException('User Authenticate error for uid=' + entity.uid + ', LDAP error=' + str(e))
    finally:
        if conn:        
            ldaphelper.close_user(conn)
    if result is False:
        raise InvalidCredentials("User Authenticate invalid creds, uid=" + entity.uid)        
    return True


def search (entity):
    __validate(entity, "User Search")
    conn = None            
    userList = []
    search_filter = '(&(objectClass=' + USER_OC_NAME + ')'
    if entity.uid is not None and len(entity.uid) > 0 :
        search_filter += '(' + UID + '=' + entity.uid + ')'
    if entity.ou is not None and len(entity.ou) > 0 :
        search_filter += '(' + OU + '=' + entity.ou + ')'
    search_filter += ')'           
    try:
        conn = ldaphelper.open()
        id = conn.search(search_base, search_filter, attributes=SEARCH_ATTRS)
        response = ldaphelper.get_response(conn, id)         
        total_entries = len(response)        
    except Exception as e:
        raise LdapException('User Authenticate search LDAP error=' + str(e))    
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
    entity.uid = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][UID])
    entity.ou = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][global_ids.OU])  
    entity.internal_id = ldaphelper.get_attr_val(entry[ATTRIBUTES][global_ids.INTERNAL_ID])    
    entity.pw_policy = ldaphelper.get_attr_val(entry[ATTRIBUTES][PW_POLICY])
    entity.cn = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][global_ids.CN])
    entity.sn = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][global_ids.SN])
    entity.description = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][global_ids.DESC])
    entity.display_name = ldaphelper.get_attr_val(entry[ATTRIBUTES][DISPLAY_NAME])
    entity.employee_type = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][EMPLOYEE_TYPE])
    entity.title = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][TITLE])
    entity.reset = ldaphelper.get_bool(entry[ATTRIBUTES][IS_RESET])
    entity.system = ldaphelper.get_bool(entry[ATTRIBUTES][IS_SYSTEM])
    entity.department_number = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][DEPT_NUM])
    entity.l = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][LOCATION])
    entity.physical_delivery_office_name = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][PHYSICAL_OFFICE_NM])
    entity.postal_code = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][POSTAL_CODE])
    entity.room_number = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][RM_NUM])

    # Get the attr as object:
    entity.locked_time = ldaphelper.get_attr_object(entry[ATTRIBUTES][LOCKED_TIME])

    # Get the multi-occurring attrs:
    entity.props = ldaphelper.get_list(entry[ATTRIBUTES][global_ids.PROPS])    
    entity.phones = ldaphelper.get_list(entry[ATTRIBUTES][TELEPHONE_NUMBER])
    entity.mobiles = ldaphelper.get_list(entry[ATTRIBUTES][MOBILE])
    entity.emails = ldaphelper.get_list(entry[ATTRIBUTES][MAIL])
    entity.roles = ldaphelper.get_list(entry[ATTRIBUTES][ROLES])
    
    # unload raw user constraint:
    entity.constraint = Constraint(ldaphelper.get_attr_val(entry[ATTRIBUTES][global_ids.CONSTRAINT]))
    
    # now, unload raw user-role constraints:    
    rcsRaw = ldaphelper.get_list(entry[ATTRIBUTES][ROLE_CONSTRAINTS])
    if rcsRaw is not None :
        entity.role_constraints = []
        for rcRaw in rcsRaw :
            entity.role_constraints.append(Constraint(rcRaw))
                        
    return entity


def create ( entity ):
    __validate(entity, 'Create User')
    try:
        attrs = {}
        attrs.update( {UID : entity.uid} )
        # generate random id:
        entity.internal_id = str(uuid.uuid4())
        attrs.update( {global_ids.INTERNAL_ID : entity.internal_id} )        
        # cn is req'd for iNetOrgPerson, if caller did not set, use uid value
        if entity.cn is None or len(entity.cn) == 0 :
            entity.cn = entity.uid
        attrs.update( {global_ids.CN : entity.cn} )
        # likewise sn is req'd for iNetOrgPerson, if caller did not set, use uid value
        if entity.sn is None or len(entity.sn) == 0 :
            entity.sn = entity.uid
        attrs.update( {global_ids.SN : entity.sn} )
                
        if entity.password is not None and len(entity.password) > 0 :                
            attrs.update( {PW : entity.password} )
        if entity.description is not None and len(entity.description) > 0 :        
            attrs.update( {global_ids.DESC : entity.description} )
        if entity.ou is not None and len(entity.ou) > 0 :        
            attrs.update( {global_ids.OU : entity.ou} )
        if entity.display_name is not None and len(entity.display_name) > 0 :        
            attrs.update( {DISPLAY_NAME : entity.display_name} )
        if entity.employee_type is not None and len(entity.employee_type) > 0 :        
            attrs.update( {EMPLOYEE_TYPE : entity.employee_type} )
        if entity.title is not None and len(entity.title) > 0 :        
            attrs.update( {TITLE : entity.title} )
        if entity.phones is not None and len(entity.phones) > 0 :        
            attrs.update( {TELEPHONE_NUMBER : entity.phones} )
        if entity.mobiles is not None and len(entity.mobiles) > 0 :        
            attrs.update( {MOBILE : entity.mobiles} )
        if entity.emails is not None and len(entity.emails) > 0 :        
            attrs.update( {MAIL : entity.emails} )
        if entity.system is not None :        
            attrs.update( {IS_SYSTEM : entity.system} )
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : entity.props} )
        if entity.department_number is not None and len(entity.department_number) > 0 :        
            attrs.update( {DEPT_NUM : entity.department_number} )
        if entity.l is not None and len(entity.l) > 0 :        
            attrs.update( {LOCATION : entity.l} )
        if entity.physical_delivery_office_name is not None and len(entity.physical_delivery_office_name) > 0 :        
            attrs.update( {PHYSICAL_OFFICE_NM : entity.physical_delivery_office_name} )
        if entity.postal_code is not None and len(entity.postal_code) > 0 :        
            attrs.update( {POSTAL_CODE : entity.postal_code} )
        if entity.room_number is not None and len(entity.room_number) > 0 :        
            attrs.update( {RM_NUM : entity.room_number} )            
        if entity.constraint is not None :        
            attrs.update( {global_ids.CONSTRAINT : entity.constraint.get_raw()} )
        if entity.pw_policy is not None and len(entity.pw_policy) > 0 :        
            attrs.update( {PW_POLICY : entity.pw_policy} )
            
#         if entity.role_constraints is not None and len(entity.role_constraints) > 0:
#             role_constraints_raw = []
#             entity.roles = []
#             for role_constraint in entity.role_constraints:
#                 role_constraints_raw.append(role_constraint.get_raw())
#                 entity.roles.append(role_constraint.name)                            
#             attrs.update( {ROLE_CONSTRAINTS : role_constraints_raw} )
#             attrs.update( {ROLES : entity.roles} )
            
        conn = ldaphelper.open()        
        id = conn.add(__get_dn(entity), USER_OCS, attrs)
    except Exception as e:
        raise LdapException('User create error=' + str(e), global_ids.USER_ADD_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.OBJECT_ALREADY_EXISTS:
            raise LdapException('User create failed, already exists:' + entity.name, global_ids.USER_ADD_FAILED)             
        elif result != 0:
            raise LdapException('User create failed result=' + str(result), global_ids.USER_ADD_FAILED)                    
    return entity


def update ( entity ):
    __validate(entity, 'Update User')
    try:
        attrs = {}                
        if entity.cn is not None or len(entity.cn) > 0 :
            attrs.update( {global_ids.CN : [(MODIFY_REPLACE, [entity.cn])]} )
        if entity.sn is not None or len(entity.sn) > 0 :
            attrs.update( {global_ids.SN : [(MODIFY_REPLACE, [entity.sn])]} )
        if entity.password is not None and len(entity.password) > 0 :                
            attrs.update( {PW : [(MODIFY_REPLACE, [entity.password])]} )
        if entity.description is not None and len(entity.description) > 0 :        
            attrs.update( {global_ids.DESC : [(MODIFY_REPLACE, [entity.description])]} )
        if entity.ou is not None and len(entity.ou) > 0 :        
            attrs.update( {global_ids.OU : [(MODIFY_REPLACE, [entity.ou])]} )
        if entity.display_name is not None and len(entity.display_name) > 0 :        
            attrs.update( {DISPLAY_NAME : [(MODIFY_REPLACE, [entity.display_name])]} )
        if entity.employee_type is not None and len(entity.employee_type) > 0 :        
            attrs.update( {EMPLOYEE_TYPE : [(MODIFY_REPLACE, entity.employee_type)]} )
        if entity.title is not None and len(entity.title) > 0 :        
            attrs.update( {TITLE : [(MODIFY_REPLACE, [entity.title])]} )
        if entity.phones is not None and len(entity.phones) > 0 :        
            attrs.update( {TELEPHONE_NUMBER : [(MODIFY_REPLACE, entity.phones)]} )           
        if entity.mobiles is not None and len(entity.mobiles) > 0 :        
            attrs.update( {MOBILE : [(MODIFY_REPLACE, entity.mobiles)]} )
        if entity.emails is not None and len(entity.emails) > 0 :        
            attrs.update( {MAIL : [(MODIFY_REPLACE, entity.emails)]} )
        if entity.system is not None :        
            attrs.update( {IS_SYSTEM : [(MODIFY_REPLACE, entity.system)]} )
        if entity.props is not None and len(entity.props) > 0 :        
            attrs.update( {global_ids.PROPS : [(MODIFY_REPLACE, entity.props)]} )
        if entity.department_number is not None and len(entity.department_number) > 0 :        
            attrs.update( {DEPT_NUM : [(MODIFY_REPLACE, entity.department_number)]} )
        if entity.l is not None and len(entity.l) > 0 :        
            attrs.update( {LOCATION : [(MODIFY_REPLACE, entity.l)]} )
        if entity.physical_delivery_office_name is not None and len(entity.physical_delivery_office_name) > 0 :        
            attrs.update( {PHYSICAL_OFFICE_NM : [(MODIFY_REPLACE, entity.physical_delivery_office_name)]} )
        if entity.postal_code is not None and len(entity.postal_code) > 0 :        
            attrs.update( {POSTAL_CODE : [(MODIFY_REPLACE, entity.postal_code)]} )
        if entity.room_number is not None and len(entity.room_number) > 0 :        
            attrs.update( {RM_NUM : [(MODIFY_REPLACE, entity.room_number)]} )            
        if entity.constraint is not None :        
            attrs.update( {global_ids.CONSTRAINT : [(MODIFY_REPLACE, entity.constraint.get_raw())]} )
        if entity.pw_policy is not None and len(entity.pw_policy) > 0 :        
            attrs.update( {PW_POLICY : [(MODIFY_REPLACE, entity.pw_policy)]} )
        if len(attrs) > 0:            
            conn = ldaphelper.open()                
            id = conn.modify(__get_dn(entity), attrs)
    except Exception as e:
        raise LdapException('User update error=' + str(e), global_ids.USER_UPDATE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise LdapException('User update failed, not found:' + entity.name, global_ids.USER_UPDATE_FAILED)             
        elif result != 0:
            raise LdapException('User update failed result=' + str(result), global_ids.USER_UPDATE_FAILED)                    
    return entity


def delete ( entity ):
    __validate(entity, 'Delete User')
    try:
        conn = ldaphelper.open()        
        id = conn.delete(__get_dn(entity))
    except Exception as e:
        raise LdapException('User delete error=' + str(e), global_ids.USER_DELETE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise LdapException('User delete not found:' + entity.name, global_ids.USER_DELETE_FAILED)                    
        elif result != 0:
            raise LdapException('User delete failed result=' + str(result), global_ids.USER_DELETE_FAILED)                    
    return entity


def __validate(entity, op):
    if entity.uid is None or len(entity.uid) == 0 :
        __raise_exception(op, UID)

                    
def __raise_exception(operation, field):
    raise LdapException('userdao.' + operation + ' required field missing:' + field)


def __get_dn(entity):
    return UID + '=' + entity.uid + ',' + search_base


USER_OC_NAME = 'inetOrgPerson'
USER_ATTRS_OC_NAME = 'ftUserAttrs'
USER_OCS = [USER_OC_NAME, USER_ATTRS_OC_NAME, global_ids.PROP_OC_NAME]

UID = 'uid'
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
    UID, global_ids.OU, global_ids.INTERNAL_ID, ROLES, ROLE_CONSTRAINTS, PW_POLICY, global_ids.CONSTRAINT,
    global_ids.CN, global_ids.SN, global_ids.DESC, DISPLAY_NAME, EMPLOYEE_TYPE,
    TITLE, TELEPHONE_NUMBER, MOBILE, MAIL, IS_RESET,
    LOCKED_TIME, IS_SYSTEM, global_ids.PROPS, DEPT_NUM,
    PHYSICAL_OFFICE_NM, POSTAL_CODE, RM_NUM, LOCATION
    ]

ATTRIBUTES = 'attributes'
search_base = Config.get('dit')['users']