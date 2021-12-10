'''
Created on Mar 21, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from ..ldap import ldaphelper, NotFound, NotUnique
from ..util import Config, global_ids
from ..util import FortressError
from ..util import logger


def create_ou (name, desc=None):
    __validate(name) 
    try:
        attrs = {}
        attrs.update( {OU_NAME : name} )
        if not desc:
            desc = 'py-fortress Container ' + name
        attrs.update( {global_ids.DESC : desc} )
        conn = ldaphelper.open()  
        id = conn.add(ldaphelper.get_container_dn(name), OU_OCS, attrs)
    except Exception as e:
        raise FortressError(msg='OU create error=' + str(e), id=global_ids.CNTR_CREATE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.OBJECT_ALREADY_EXISTS:
            raise NotUnique(msg='OU create failed, already exists:' + name, id=global_ids.CNTR_ALREADY_EXISTS)             
        elif result != 0:
            raise FortressError(msg='OU create failed result=' + str(result), id=global_ids.CNTR_CREATE_FAILED)


def delete_ou ( name ):
    __validate(name)   
    try:
        conn = ldaphelper.open()       
        id = conn.delete(ldaphelper.get_container_dn(name))
    except Exception as e:
        raise FortressError(msg='OU delete error=' + str(e), id=global_ids.CNTR_DELETE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='OU delete not found:' + name, id=global_ids.CNTR_NOT_FOUND)                    
        elif result != 0:
            raise FortressError(msg='OU delete failed result=' + str(result), id=global_ids.CNTR_DELETE_FAILED)


def create_suffix ( name ):
    dn = DC_NAME + '=' + name + ',' + DC_NAME + '=com'
    try:
        attrs = {}
        attrs.update( {DC_NAME : name} )
        attrs.update( {O : name} )
        conn = ldaphelper.open()        
        id = conn.add(dn, SUFX_OCS, attrs)
    except Exception as e:
        raise FortressError(msg='Suffix create dn=' + dn + ', error=' + str(e), id=global_ids.SUFX_CREATE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.OBJECT_ALREADY_EXISTS:
            raise NotUnique(msg='Suffix create failed, already exists:' + dn, id=global_ids.SUFX_ALREADY_EXISTS)             
        elif result != 0:
            raise FortressError(msg='Suffix create failed, dn=' + dn + ', result=' + str(result), id=global_ids.SUFX_CREATE_FAILED)


def delete_suffix ():
    try:
        conn = ldaphelper.open()        
        id = conn.delete(__SUFX_DN)
    except Exception as e:
        raise FortressError(msg='Suffix delete failed, dn=' + __SUFX_DN + ', error=' + str(e), id=global_ids.SUFX_DELETE_FAILED)
    else:
        result = ldaphelper.get_result(conn, id)
        if result == global_ids.NOT_FOUND:
            raise NotFound(msg='Suffix delete not found dn=' + __SUFX_DN, id=global_ids.SUFX_NOT_EXIST)                    
        elif result != 0:
            raise FortressError(msg='Suffix delete failed, dn=' + __SUFX_DN + ', result=' + str(result), id=global_ids.SUFX_DELETE_FAILED)


def bootstrap ():
    suffix_nm = __get_rdn_name(__SUFX_DN)
    try:
        create_suffix ( suffix_nm )
    except NotUnique:
        logger.warn('create suffix failed, already present, name=' + suffix_nm)
    try:
        create_ou (global_ids.USER_OU)
    except NotUnique:
        logger.warn('create users container failed, already present')
    try:
        create_ou (global_ids.ROLE_OU)
    except NotUnique:
        logger.warn('create roles container failed, already present')
    try:
        create_ou (global_ids.PERM_OU)
    except NotUnique:
        logger.warn('create perms container failed, already present')    
 
 
def __validate(name):
    if not name:
        raise FortressError(msg='OU name null', id=global_ids.CNTR_NAME_NULL)

 
def __get_rdn_name(dn):
    name = None
    values = dn.split(',')        
    values = [ val.strip() for val in values ]
    if values[0] is not None:
        name=values[0]
    return name[3:]  
 
  
# suffix:
__SUFX_DN = Config.get(global_ids.DIT)[global_ids.SUFFIX]
DC_OC_NAME = 'dcObject'
ORG_OC_NAME = 'organization'
SUFX_OCS = [DC_OC_NAME, ORG_OC_NAME]
DC_NAME = 'dc'
O = 'o'

# orgunit:
OU_OC_NAME = 'organizationalUnit'
OU_OCS = [OU_OC_NAME]
OU_NAME = 'ou'
