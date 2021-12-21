'''
@copyright: 2022 - Symas Corporation
'''
from ..model import User
from crypt import crypt
from hmac import compare_digest

from ..util.fortress_error import RbacError
from ..file.fileex import AuthError,AuthFail
from ..file.common import require_one,attrs,common_search

def read (entity):
    return require_one('User', search(entity), entity.uid)

def authenticate (entity):
    try:
        user = read(entity)
        if (user.password is None
            or len(user.password) == 0
            or entity.password is None
            or len(entity.password) == 0
            or not compare_digest(
                user.password,
                crypt(entity.password, salt=user.password) )):
            raise AuthFail()
    except AuthFail as a:
        raise a
    except RbacError as f: # May need to check more cases
        raise AuthFail()
    except Exception as e:
        raise AuthError(msg="auth error: "+str(e))
    return True

def search (entity):
    return map(lambda e:__unload(e), common_search('user', entity))

def __unload(entry):
    entity = User()
    for attr in attrs["search"]["user"] + attrs["search_multi"]["user"] + attrs["extra"]["user"]:
        setattr(entity, attr, entry.get(attr))
    return entity

