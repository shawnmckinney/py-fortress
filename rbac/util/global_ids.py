'''
@copyright: 2022 - Symas Corporation
'''

# config file ENV VAR:
PYFORTRESS_CONF = "PYFORTRESS_CONF"

# config attribute names
ATTRIBUTES = 'attributes'
USER_OU = 'users'
ROLE_OU = 'roles'
PERM_OU = 'perms'
SUFFIX = 'suffix'
DIT = 'dit'
      

UID = 'uid'
PROP_OC_NAME = 'ftProperties'
OU = 'ou'
INTERNAL_ID = 'ftid'
CN = 'cn'
SN = 'sn'
DN = 'dn'
CONSTRAINT = 'ftCstr'
DESC = 'description'
PROPS = 'ftProps'
CONSTRAINT = 'ftCstr'

SUCCESS = 0
OBJECT_ALREADY_EXISTS = 68
NOT_FOUND = 32
NO_SUCH_ATTRIBUTE = 16
NOT_ALLOWED_ON_NONLEAF = 66
CONFIG_BOOTSTRAP_FAILED = 126

ROLE_ALREADY_ACTIVATED_ERROR = 2001
ROLE_NOT_ACTIVATED_ERROR = 2002

USER_SEARCH_FAILED = 1000
USER_READ_FAILED = 1001
USER_ADD_FAILED = 1002
USER_UPDATE_FAILED = 1003
USER_DELETE_FAILED = 1004
USER_NOT_FOUND = 1005
USER_ID_NULL = 1006
USER_NULL = 1008
USER_PW_INVLD = 1013
USER_PW_CHK_FAILED = 1014
USER_SESS_NULL = 1030

URLE_NULL = 2003
URLE_ASSIGN_FAILED = 2004
URLE_DEASSIGN_FAILED = 2005
URLE_ACTIVATE_FAILED = 2006
URLE_DEACTIVE_FAILED = 2007
URLE_ASSIGN_EXIST = 2008
URLE_ASSIGN_NOT_EXIST = 2009
URLE_SEARCH_FAILED = 2010
URLE_ALREADY_ACTIVE = 2011
URLE_NOT_ACTIVE = 2022

ACTV_FAILED_DAY = 2050
ACTV_FAILED_DATE = 2051
ACTV_FAILED_TIME = 2052
ACTV_FAILED_TIMEOUT = 2053
ACTV_FAILED_LOCK = 2054

PERM_SEARCH_FAILED = 3000
PERM_READ_OP_FAILED = 3001
PERM_READ_OBJ_FAILED = 3002
PERM_ADD_FAILED = 3003
PERM_UPDATE_FAILED = 3004
PERM_DELETE_FAILED = 3005
PERM_NULL = 3008
PERM_OPERATION_NULL = 3009
PERM_OBJECT_NULL = 3010
PERM_OBJECT_NM_NULL = 3027
PERM_OPERATION_NM_NULL = 3026
PERM_GRANT_FAILED = 3012
PERM_REVOKE_FAILED = 3024
PERM_OP_NOT_FOUND = 3006
PERM_OBJ_NOT_FOUND = 3007
PERM_DUPLICATE = 3011
PERM_ROLE_NOT_EXIST = 3016
PERM_ROLE_SEARCH_FAILED = 3019
PERM_NOT_EXIST = 3029
PERM_OBJECT_DELETE_FAILED_NONLEAF = 3050

ROLE_SEARCH_FAILED = 5000
ROLE_READ_FAILED = 5001
ROLE_ADD_FAILED = 5002
ROLE_UPDATE_FAILED = 5003
ROLE_DELETE_FAILED = 5004
ROLE_NM_NULL = 5005
ROLE_NOT_FOUND = 5006
ROLE_NULL = 5007
ROLE_USER_ASSIGN_FAILED = 5008
ROLE_USER_DEASSIGN_FAILED = 5009
ROLE_LST_NULL = 5010
ROLE_OCCUPANT_SEARCH_FAILED = 5011
ROLE_REMOVE_OCCUPANT_FAILED = 5012

CNTR_CREATE_FAILED = 6001
CNTR_DELETE_FAILED = 6002
CNTR_NAME_NULL = 6003
CNTR_NAME_INVLD = 6004
CNTR_PARENT_NULL = 6005
CNTR_PARENT_INVLD = 6006
CNTR_NOT_FOUND = 6007
CNTR_ALREADY_EXISTS = 6008

SUFX_CREATE_FAILED = 6010
SUFX_DELETE_FAILED = 6011
SUFX_NAME_NULL = 6012
SUFX_ALREADY_EXISTS = 6016
SUFX_NOT_EXIST = 6017