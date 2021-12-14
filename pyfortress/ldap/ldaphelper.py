'''
Created on Feb 11, 2018

@author: smckinney
@copyright: 2018 - Symas Corporation
'''

import logging
import ldap
import ldapurl
from ..util import global_ids
from ..ldap import LdapException
from ..util import Config
from ..util import logger


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
        c = ldap.initialize(_uri)
        c.bind_s(user_dn, password)
    except Exception as e:
        raise LdapException ('connutl.open Exception=' + str (e))
    if(_ldap_debug):
        logger.debug(c.usage)        
    return c


def _open_admin ():
    try:
        c = ldap.initialize(_uri)
        c.bind_s(_service_uid, _service_pw)
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
_ldap_debug = Config.get(LDAP)['debug']
_pool_name = Config.get(LDAP)['pool_name']
_pool_size = int(Config.get(LDAP)['pool_size'])
_pool_lifetime = int(Config.get(LDAP)['pool_lifetime'])
_pool_keepalive = int(Config.get(LDAP)['pool_keepalive'])
_ldap_use_ssl = Config.get(LDAP)['use_ssl']
_ldap3_log_level_str = Config.get(LDAP)['ldap3_log_level']
_ldap3_log_level = 0

if 'uri' in Config.get(LDAP):
    _uri = Config.get(LDAP)['uri']
else:
    hostport = [Config.get(LDAP)['host']]
    if 'port' in Config.get(LDAP):
        hostport.append(str(Config.get(LDAP)['port']))
    _uri = ldapurl.LDAPUrl(hostport=":".join(hostport)).unparse()

logger.info('Initialize py-fortress ldap...')
logger.info('ldap url: ' + _uri)

# Needed for server/connection pooling:
#_srv1 = ldap3.Server(host=_ldap_host, port=_ldap_port, connect_timeout=_ldap_timeout, use_ssl=_ldap_use_ssl)
#_srv_pool = ldap3.ServerPool([_srv1], ldap3.ROUND_ROBIN, exhaust=True, active=True)
#_usr_pool = ldap3.ServerPool([_srv1], ldap3.ROUND_ROBIN, exhaust=True, active=True)

__SUFX_DN = Config.get('dit')['suffix']
