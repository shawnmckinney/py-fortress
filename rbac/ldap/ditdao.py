'''
@copyright: 2022 - Symas Corporation
'''

import ldap
from rbac.ldap import ldaphelper, NotFound, NotUnique
from rbac.ldap.ldaphelper import add_to_modlist
from rbac.util import Config, global_ids
from rbac.util.fortress_error import RbacError
from rbac.util import logger


def create_ou (name, desc=None):
    __validate(name) 
    try:
        attrs = {}
        attrs.update( {'objectClass': OU_OCS} )
        attrs.update( {OU_NAME : name} )
        if not desc:
            desc = 'py-fortress Container ' + name
        attrs.update( {global_ids.DESC : desc} )
        conn = ldaphelper.open()  
        conn.add_s(ldaphelper.get_container_dn(name), add_to_modlist(attrs))
    except Exception as e:
        raise RbacError(msg='OU create error=' + str(e), id=global_ids.CNTR_CREATE_FAILED)
    except ldap.ALREADY_EXISTS:
        raise NotUnique(msg='OU create failed, already exists:' + name, id=global_ids.CNTR_ALREADY_EXISTS)
    except ldap.LDAPError as e:
        raise RbacError(msg='OU create failed result=' + str(e), id=global_ids.CNTR_CREATE_FAILED)


def delete_ou ( name ):
    __validate(name)   
    try:
        conn = ldaphelper.open()       
        conn.delete_s(ldaphelper.get_container_dn(name))
    except ldap.NO_SUCH_OBJECT:
        raise NotFound(msg='OU delete not found:' + name, id=global_ids.CNTR_NOT_FOUND)
    except ldap.LDAPError as e:
        raise RbacError(msg='OU delete failed result=' + str(e), id=global_ids.CNTR_DELETE_FAILED)
    except Exception as e:
        raise RbacError(msg='OU delete error=' + str(e), id=global_ids.CNTR_DELETE_FAILED)


def create_suffix ( name ):
    dn = DC_NAME + '=' + name + ',' + DC_NAME + '=com'
    try:
        attrs = {}
        attrs.update( {'objectClass': SUFX_OCS} )
        attrs.update( {DC_NAME : name} )
        attrs.update( {O : name} )
        conn = ldaphelper.open()        
        conn.add_s(dn, add_to_modlist(attrs))
    except Exception as e:
        raise NotUnique(msg='Suffix create failed, already exists:' + dn, id=global_ids.SUFX_ALREADY_EXISTS)
    except ldap.ALREADY_EXISTS:
        raise RbacError(msg='Suffix create failed, dn=' + dn + ', result=' + str(e), id=global_ids.SUFX_CREATE_FAILED)
    except Exception as e:
        raise RbacError(msg='Suffix create dn=' + dn + ', error=' + str(e), id=global_ids.SUFX_CREATE_FAILED)


def delete_suffix ():
    try:
        conn = ldaphelper.open()        
        conn.delete_s(__SUFX_DN)
    except ldap.NO_SUCH_OBJECT:
        raise NotFound(msg='Suffix delete not found dn=' + __SUFX_DN, id=global_ids.SUFX_NOT_EXIST)
    except ldap.LDAPError as e:
        raise RbacError(msg='Suffix delete failed, dn=' + __SUFX_DN + ', result=' + str(e), id=global_ids.SUFX_DELETE_FAILED)
    except Exception as e:
        raise RbacError(msg='Suffix delete failed, dn=' + __SUFX_DN + ', error=' + str(e), id=global_ids.SUFX_DELETE_FAILED)


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
        raise RbacError(msg='OU name null', id=global_ids.CNTR_NAME_NULL)

 
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
