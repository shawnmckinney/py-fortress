'''
Created on Feb 10, 2018

@author: smckinney
'''

from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
import user
import ldaphelper, daoex
from config import Config
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
        raise daoex.FortressException('Exception in userdao.search=' + str(e))
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
    
    entity = user.User()
    entity.dn = ldaphelper.get_dn(entry)        
    entity.uid = ldaphelper.get_attr(entry[ATTRIBUTES][UID])
    entity.ou = ldaphelper.get_attr(entry[ATTRIBUTES][OU])  
    entity.ou = ldaphelper.get_attr(entry[ATTRIBUTES][OU])
    entity.internalId = ldaphelper.get_attr(entry[ATTRIBUTES][INTERNAL_ID])            
    entity.roles = ldaphelper.get_attr(entry[ATTRIBUTES][ROLES])
    entity.pwPolicy = ldaphelper.get_attr(entry[ATTRIBUTES][PW_POLICY])
    entity.cn = ldaphelper.get_attr(entry[ATTRIBUTES][CN])
    entity.sn = ldaphelper.get_attr(entry[ATTRIBUTES][SN])
    entity.description = ldaphelper.get_attr(entry[ATTRIBUTES][DESCRIPTION])
    
#     entity.x = ldaphelper.get_attr(entry[ATTRIBUTES][x])
#     entity.x = ldaphelper.get_attr(entry[ATTRIBUTES][x])
#     entity.x = ldaphelper.get_attr(entry[ATTRIBUTES][x])
#     entity.x = ldaphelper.get_attr(entry[ATTRIBUTES][x])
#     entity.x = ldaphelper.get_attr(entry[ATTRIBUTES][x])
#     entity.x = ldaphelper.get_attr(entry[ATTRIBUTES][x])
#     entity.x = ldaphelper.get_attr(entry[ATTRIBUTES][x])
#     entity.x = ldaphelper.get_attr(entry[ATTRIBUTES][x])
    return entity


def validate(entity, op):
    if entity.uid is None or len(entity.uid) == 0 :
        raise_exception(op, UID)

                    
def raise_exception(operation, field):
    raise daoex.FortressException('userdao.' + operation + ' required field missing:' + field)


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
DESCRIPTION = 'description'

ATTRIBUTES = 'attributes'
SEARCH_ATTRS = Config.get('schema')['user']['attributes']
search_base = Config.get('dit')['users']
