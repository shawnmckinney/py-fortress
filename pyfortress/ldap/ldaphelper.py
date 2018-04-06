'''
Created on Feb 11, 2018

@author: smckinney
@copyright: 2018 - Symas Corporation
'''

import logging
import ldap3
from ldap3.utils.log import set_library_log_activation_level
set_library_log_activation_level(logging.CRITICAL)
from ldap3.utils.log import set_library_log_detail_level, OFF, ERROR, BASIC, PROTOCOL, NETWORK, EXTENDED
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
        c = ldap3.Connection(_usr_pool,
                             user=user_dn,
                             password=password,
                             client_strategy='SYNC',
                             auto_bind=False,
                             collect_usage=_ldap_debug,
                             pool_name=_pool_name + 'usr',
                             pool_size=_pool_size,
                             pool_lifetime=_pool_lifetime,
                             pool_keepalive=_pool_keepalive,
                             receive_timeout=_ldap_timeout,
                             lazy=False
                             )
    except Exception as e:
        raise LdapException ('connutl.open Exception=' + str (e))
    if(_ldap_debug):
        logger.debug(c.usage)        
    return c


def _open_admin ():
    try:
        c = ldap3.Connection(_srv_pool,
                             user=_service_uid,
                             password=_service_pw,
                             client_strategy='REUSABLE',
                             auto_bind=True,
                             collect_usage=_ldap_debug,
                             pool_name=_pool_name,
                             pool_size=_pool_size,
                             pool_lifetime=_pool_lifetime,
                             pool_keepalive=_pool_keepalive,
                             receive_timeout=_ldap_timeout,
                             lazy=False
                             )
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
    if len (lattr) > 0:
        value = str (lattr)
        #value = lattr
    return value


# Call this to get value from a single-occurring attribute:    
def get_attr_object(lattr):
    value = ""
    if lattr is not None:
        value = lattr
    return value


# Call this when expecting a single value from a multi-occurring attribute:
def get_one_attr_val(lattr):
    value = ""
    if len (lattr) > 0:
        lst = lattr
        value = lst[0]
    return value


# Call this to get a list of attribute values:
def get_list(lattr):
    value = ""
    if len (lattr) > 0:
        value = lattr
    return value


def get_bool(lattr):
    value = False
    value = str (lattr)
    return value


def get_result(conn, id):
    res = conn.get_response(id)
    return res[1].get('result')


def get_dn(entry):
    return entry['dn']

def get_container_dn(ou):
    return global_ids.OU + '=' + Config.get('dit')[ou] + ',' + __SUFX_DN


# Begin the Config section:
Config.load('py-fortress-cfg.json')
LDAP = 'ldap'
_service_uid = Config.get(LDAP)['dn']
_service_pw = Config.get(LDAP)['password']
_ldap_host = Config.get(LDAP)['host']
_ldap_port = int(Config.get(LDAP)['port'])
_ldap_timeout = int(Config.get(LDAP)['timeout'])
_ldap_debug = Config.get(LDAP)['debug']
_pool_name = Config.get(LDAP)['pool_name']
_pool_size = int(Config.get(LDAP)['pool_size'])
_pool_lifetime = int(Config.get(LDAP)['pool_lifetime'])
_pool_keepalive = int(Config.get(LDAP)['pool_keepalive'])
_ldap_use_ssl = Config.get(LDAP)['use_ssl']
_ldap3_log_level_str = Config.get(LDAP)['ldap3_log_level']
_ldap3_log_level = 0

logger.info('Initialize py-fortress ldap...')
logger.info('ldap host: ' + _ldap_host +  ', port:' + str(_ldap_port))

# Map from config string literals to ldap3 logger constants to set logger level:
if _ldap3_log_level_str == 'OFF' :
    _ldap3_log_level = OFF
elif _ldap3_log_level_str == 'ERROR' :
    _ldap3_log_level = ERROR
elif _ldap3_log_level_str == 'BASIC' :
    _ldap3_log_level = BASIC
elif _ldap3_log_level_str == 'PROTOCOL' :
    _ldap3_log_level = PROTOCOL
elif _ldap3_log_level_str == 'NETWORK' :
    _ldap3_log_level = NETWORK
elif _ldap3_log_level_str == 'EXTENDED' :
    _ldap3_log_level = EXTENDED
set_library_log_detail_level(_ldap3_log_level)

# Needed for server/connection pooling:
_srv1 = ldap3.Server(host=_ldap_host, port=_ldap_port, connect_timeout=_ldap_timeout, use_ssl=_ldap_use_ssl)
_srv_pool = ldap3.ServerPool([_srv1], ldap3.ROUND_ROBIN, exhaust=True, active=True)
_usr_pool = ldap3.ServerPool([_srv1], ldap3.ROUND_ROBIN, exhaust=True, active=True)

__SUFX_DN = Config.get('dit')['suffix']