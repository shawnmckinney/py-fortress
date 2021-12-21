'''
@copyright: 2022 - Symas Corporation
'''

from rbac.util.fortress_error import RbacError
from rbac.util import global_ids


def validate_user(user):
    if user is None:
        raise RbacError (msg='User is None', id=global_ids.USER_NULL)
    elif not user.uid:
        raise RbacError (msg='User uid is None', id=global_ids.USER_ID_NULL)


def validate_role(role):
    if role is None:
        raise RbacError (msg='Role is None', id=global_ids.ROLE_NULL)
    elif not role.name:
        raise RbacError (msg='Role name is None', id=global_ids.ROLE_NM_NULL)


def validate_perm_obj(perm):
    if perm is None:
        raise RbacError (msg='Perm object is None', id=global_ids.PERM_OBJECT_NULL)
    elif not perm.obj_name:
        raise RbacError (msg='Perm object name is None', id=global_ids.PERM_OBJECT_NM_NULL)

    
def validate_perm(perm):
    if perm is None:
        raise RbacError (msg='Permission is None', id=global_ids.PERM_OPERATION_NULL)
    elif not perm.obj_name:
        raise RbacError (msg='Permission object name is None', id=global_ids.PERM_OBJECT_NM_NULL)
    elif not perm.op_name:
        raise RbacError (msg='Permission operation name is None', id=global_ids.PERM_OPERATION_NM_NULL)
