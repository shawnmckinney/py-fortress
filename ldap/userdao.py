'''
Created on Feb 10, 2018

@author: smckinney
'''

from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
from model import User, Constraint
from ldap import ldaphelper, LdapException, NotFound, NotUnique
from util import Config

import logging


def search (entity):
    validate(entity, "User Search")
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
                userList.append(unload(entry))
    finally:
        if conn:        
            ldaphelper.close(conn)
    return userList


def unload(entry):
    
    print(entry['dn'], entry['attributes'])
    
    entity = User()
    entity.dn = ldaphelper.get_dn(entry)        
    entity.uid = ldaphelper.get_attr(entry[ATTRIBUTES][UID])
    entity.ou = ldaphelper.get_attr(entry[ATTRIBUTES][OU])  
    entity.ou = ldaphelper.get_attr(entry[ATTRIBUTES][OU])
    entity.internalId = ldaphelper.get_attr(entry[ATTRIBUTES][INTERNAL_ID])
    entity.pwPolicy = ldaphelper.get_attr(entry[ATTRIBUTES][PW_POLICY])
    entity.cn = ldaphelper.get_attr(entry[ATTRIBUTES][CN])
    entity.sn = ldaphelper.get_attr(entry[ATTRIBUTES][SN])
    entity.description = ldaphelper.get_attr(entry[ATTRIBUTES][DESCRIPTION])
    entity.displayName = ldaphelper.get_attr(entry[ATTRIBUTES][DISPLAY_NAME])
    entity.employeeType = ldaphelper.get_attr(entry[ATTRIBUTES][EMPLOYEE_TYPE])
    entity.title = ldaphelper.get_attr(entry[ATTRIBUTES][TITLE])
    entity.phones = ldaphelper.get_attr(entry[ATTRIBUTES][TELEPHONE_NUMBER])
    entity.mobiles = ldaphelper.get_attr(entry[ATTRIBUTES][MOBILE])
    entity.emails = ldaphelper.get_attr(entry[ATTRIBUTES][MAIL])
    entity.reset = ldaphelper.get_attr(entry[ATTRIBUTES][IS_RESET])
    entity.lockedTime = ldaphelper.get_attr(entry[ATTRIBUTES][LOCKED_TIME])
    entity.system = ldaphelper.get_bool(entry[ATTRIBUTES][IS_SYSTEM])
    entity.props = ldaphelper.get_attr(entry[ATTRIBUTES][PROPS])
    entity.departmentNumber = ldaphelper.get_attr(entry[ATTRIBUTES][DEPT_NUM])
    entity.l = ldaphelper.get_attr(entry[ATTRIBUTES][LOCATION])
    entity.physicalDeliveryOfficeName = ldaphelper.get_attr(entry[ATTRIBUTES][PHYSICAL_OFFICE_NM])
    entity.postalCode = ldaphelper.get_attr(entry[ATTRIBUTES][POSTAL_CODE])
    entity.roomNumber = ldaphelper.get_attr(entry[ATTRIBUTES][RM_NUM])
    entity.roles = ldaphelper.get_attr(entry[ATTRIBUTES][ROLES])
    entity.constraint = Constraint()
    entity.constraint.raw = ldaphelper.get_attr(entry[ATTRIBUTES][CONSTRAINT])
    entity.constraint.load()    
    rcsRaw = ldaphelper.get_list(entry[ATTRIBUTES][ROLE_CONSTRAINTS])
    if rcsRaw is not None :
        entity.roleConstraints = []
        for rcRaw in rcsRaw :
            constraint = Constraint()
            entity.roleConstraints.append(constraint)
            constraint.raw = rcRaw
            constraint.load()    
                                           
#     entity.x = ldaphelper.get_attr(entry[ATTRIBUTES][x])
#     entity.x = ldaphelper.get_attr(entry[ATTRIBUTES][x])
#     entity.x = ldaphelper.get_attr(entry[ATTRIBUTES][x])
    return entity


def validate(entity, op):
    if entity.uid is None or len(entity.uid) == 0 :
        raise_exception(op, UID)

                    
def raise_exception(operation, field):
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


ATTRIBUTES = 'attributes'
SEARCH_ATTRS = Config.get('schema')['user']['attributes']
search_base = Config.get('dit')['users']
