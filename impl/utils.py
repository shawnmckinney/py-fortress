'''
Created on Mar 18, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from impl.fortress_error import FortressError
from util import global_ids


def validate_user(user):
    if user is None:
        raise FortressError ('User is None')
    elif user.uid is None:
        raise FortressError ('User uid is None')


def validate_perm(perm):
    if perm is None:
        raise FortressError ('Perm is None')
    elif perm.obj_name is None:
        raise FortressError ('Perm object name is None')
    elif perm.op_name is None:
        raise FortressError ('Perm op name is None')
