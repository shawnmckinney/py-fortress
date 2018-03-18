'''
Created on Mar 18, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from impl.fortress_error import FortressError
from util import global_ids


def validate_user(user):
    if user is None:
        raise FortressError (msg='User is None', id=global_ids.USER_NULL)
    elif user.uid is None:
        raise FortressError (msg='User uid is None', id=global_ids.USER_ID_NULL)


def validate_role(role):
    if role is None:
        raise FortressError (msg='Role is None', id=global_ids.ROLE_NULL)
    elif role.name is None:
        raise FortressError (msg='Role name is None', id=global_ids.ROLE_NM_NULL)


def validate_perm_obj(perm):
    if perm is None:
        raise FortressError (msg='Perm object is None', id=global_ids.PERM_OBJECT_NULL)
    elif perm.obj_name is None:
        raise FortressError (msg='Perm object name is None', id=global_ids.PERM_OBJECT_NM_NULL)

    
def validate_perm(perm):
    if perm is None:
        raise FortressError (msg='Permission is None', id=global_ids.PERM_OPERATION_NULL)
    elif perm.obj_name is None:
        raise FortressError (msg='Permission object name is None', id=global_ids.PERM_OBJECT_NM_NULL)
    elif perm.op_name is None:
        raise FortressError (msg='Permission operation name is None', id=global_ids.PERM_OPERATION_NM_NULL)
