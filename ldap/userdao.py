'''
Created on Feb 10, 2018

@author: smckinney
@copyright: 2018 - Symas Corporation
'''
    
from model import User, Constraint
from ldap import ldaphelper, LdapException, NotFound, NotUnique, InvalidCredentials
from util import Config


def read (entity):
    userList = search(entity)
    if userList is None or len(userList) == 0:
        raise NotFound()
    elif len(userList) > 1:
        raise NotUnique()
    else:
        return userList[0]


def authenticate (entity):
    __validate(entity, "User Bind")
    conn = None
    result = False            
    try:        
        conn = ldaphelper.open_user(UID + '=' + entity.uid + ',' + search_base, entity.password)
        result = conn.bind()
    except Exception as e:
        raise LdapException('Exception in userdao.authenticate=' + str(e))
    finally:
        if conn:        
            ldaphelper.close(conn)
    if result is False:
        raise InvalidCredentials        
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
        raise LdapException('Exception in userdao.search=' + str(e))
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
    entity.ou = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][OU])  
    entity.internal_id = ldaphelper.get_attr_val(entry[ATTRIBUTES][INTERNAL_ID])    
    entity.pw_policy = ldaphelper.get_attr_val(entry[ATTRIBUTES][PW_POLICY])
    entity.cn = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][CN])
    entity.sn = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][SN])
    entity.description = ldaphelper.get_one_attr_val(entry[ATTRIBUTES][DESCRIPTION])
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
    entity.props = ldaphelper.get_list(entry[ATTRIBUTES][PROPS])    
    entity.phones = ldaphelper.get_list(entry[ATTRIBUTES][TELEPHONE_NUMBER])
    entity.mobiles = ldaphelper.get_list(entry[ATTRIBUTES][MOBILE])
    entity.emails = ldaphelper.get_list(entry[ATTRIBUTES][MAIL])
    entity.roles = ldaphelper.get_list(entry[ATTRIBUTES][ROLES])
    
    # unload raw user constraint:
    entity.constraint = Constraint(ldaphelper.get_attr_val(entry[ATTRIBUTES][CONSTRAINT]))
    
    # now, unload raw user-role constraints:    
    rcsRaw = ldaphelper.get_list(entry[ATTRIBUTES][ROLE_CONSTRAINTS])
    if rcsRaw is not None :
        entity.role_constraints = []
        for rcRaw in rcsRaw :
            entity.role_constraints.append(Constraint(rcRaw))
                        
    return entity


def __validate(entity, op):
    if entity.uid is None or len(entity.uid) == 0 :
        __raise_exception(op, UID)

                    
def __raise_exception(operation, field):
    raise LdapException('userdao.' + operation + ' required field missing:' + field)


USER_OC_NAME = 'inetOrgPerson'
UID = 'uid'
OU = 'ou'
PW = 'pw'
INTERNAL_ID = 'ftid'
ROLES = 'ftra'
PW_POLICY = 'pwdPolicySubentry'
CN = 'cn'
SN = 'sn'
DN = 'dn'
CONSTRAINT = 'ftCstr'
ROLE_CONSTRAINTS = 'ftRC'
DESCRIPTION = 'description'
DISPLAY_NAME = 'displayName'
EMPLOYEE_TYPE = 'employeeType'
TITLE = 'title'
TELEPHONE_NUMBER = 'telephoneNumber'
MOBILE = 'mobile'
MAIL = 'mail'
IS_RESET = 'pwdReset'
LOCKED_TIME = 'pwdAccountLockedTime'
IS_SYSTEM = 'ftSystem'
PROPS = 'ftProps'
DEPT_NUM = 'departmentNumber'
LOCATION = 'l'
PHYSICAL_OFFICE_NM = 'physicalDeliveryOfficeName'
POSTAL_CODE = 'postalCode'
RM_NUM = 'roomNumber'

SEARCH_ATTRS = [
    UID, OU, INTERNAL_ID, ROLES, ROLE_CONSTRAINTS, PW_POLICY, CONSTRAINT,
    CN, SN, DESCRIPTION, DISPLAY_NAME, EMPLOYEE_TYPE,
    TITLE, TELEPHONE_NUMBER, MOBILE, MAIL, IS_RESET,
    LOCKED_TIME, IS_SYSTEM, PROPS, DEPT_NUM,
    PHYSICAL_OFFICE_NM, POSTAL_CODE, RM_NUM, LOCATION
    ]

ATTRIBUTES = 'attributes'
search_base = Config.get('dit')['users']