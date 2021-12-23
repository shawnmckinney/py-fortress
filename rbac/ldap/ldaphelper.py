'''
@copyright: 2022 - Symas Corporation
'''

from rbac.util import global_ids
from rbac.ldap import LdapException
from rbac.util import Config
from rbac.util import logger
from ldappool import ConnectionManager


# Open a connection for a particular user:
def open_user (user_dn, password):
    c = _open_user(user_dn, password)    
    return c

# Open a connection from the pool with service accounts:
def open ():
    c = _open_admin()
    if(_ldap_debug):
        logger.debug(c.usage)        
    return c

def _open_user (user_dn, password):
    try:
        with _srv_pool.connection(user_dn, password) as conn:
            c = conn
    except Exception as e:
        raise LdapException ('connutl.open Exception=' + str (e))
    if(_ldap_debug):
        logger.debug(c.usage)        
    return c


def _open_admin ():
    try:
        with _srv_pool.connection() as conn:
            c = conn
    except Exception as e:
        raise LdapException ('connutl.open Exception=' + str (e))
    if(_ldap_debug):
        logger.debug(c.usage)        
    return c


def close (conn):
    pass
    #conn.unbind()


def close_user (conn):
    conn.unbind()


def get_response(conn, id):
    res = conn.get_response(id)
    return res[0] 

    
# Call this to get value from a single-occurring attribute:    
def get_attr_val(lattr):
    value = ""
    if lattr:
        value = lattr[0].decode()
    return value


# Call this to get value from a single-occurring attribute:    
def get_attr_object(lattr):
    value = ""
    if lattr:
        value = lattr[0].decode()
    return value


# Call this when expecting a single value from a multi-occurring attribute:
def get_one_attr_val(lattr):
    if not lattr:
        return "" # FIXME: really?
    return lattr[0].decode()


# Call this to get a list of attribute values:
def get_list(lattr):
    return [value.decode() for value in lattr]


def get_bool(lattr, default=False):
    if not lattr:
        return default
    return (lattr[0].decode() == 'TRUE')


def get_result(conn, id):
    res = conn.get_response(id)
    return res[1].get('result')


def get_dn(entry):
    return entry['dn']

def get_container_dn(ou):
    return global_ids.OU + '=' + Config.get('dit')[ou] + ',' + __SUFX_DN


def add_to_modlist(attrs):
    result = []
    for attr, vals in attrs.items():
        if not isinstance(vals, (tuple, list)):
            vals = [vals]
        vals = [v.encode() if isinstance(v, str) else v for v in vals]
        result.append((attr, vals))
    return result


def mods_to_modlist(attrs):
    result = []
    for attr, mods in attrs.items():
        for op, vals in mods:
            if not isinstance(vals, (tuple, list)):
                vals = [vals]
            vals = [v.encode() if isinstance(v, str) else v for v in vals]
            result.append((op, attr, vals))
    return result


# Begin the Config section:
Config.load('py-fortress-cfg.json')
LDAP = 'ldap'
_service_uid = Config.get(LDAP)['dn']
_service_pw = Config.get(LDAP)['password']
_ldap_timeout = int(Config.get(LDAP)['timeout'])
_pool_size = int(Config.get(LDAP)['pool_size'])
_ldap_use_tls = Config.get(LDAP)['use_tls']
_uri = Config.get(LDAP)['uri']
_ldap_debug = Config.get(LDAP)['debug']

_srv_pool = ConnectionManager(_uri, size=_pool_size, bind=_service_uid, passwd=_service_pw, timeout=_ldap_timeout, use_tls=_ldap_use_tls)
_usr_pool = ConnectionManager(_uri, size=_pool_size, timeout=_ldap_timeout, use_tls=_ldap_use_tls)
__SUFX_DN = Config.get('dit')['suffix']
