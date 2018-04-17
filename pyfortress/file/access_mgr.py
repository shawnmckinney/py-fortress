from contextlib import contextmanager

from ..model import Session,User,Role
from ..util import Date
from ..util import Day
from ..util import LockDate
from ..util import Time
from ..util import TimeOut
from ..util import CurrentDateTime
from . import userdao,permdao
from ..util import FortressError
from ..util import logger
from ..util import global_ids
from ..util import SUCCESS

@contextmanager
def _valid (thing, field, name, id=None):
    if thing is None or getattr(thing,field,None) is None:
        raise FortressError (msg="{} is None".format(name), id=id)
    logger.debug ('opening {} {}'.format(name, getattr(thing,field)))
    yield thing
    logger.debug ('closing {} {}'.format(name, getattr(thing,field)))

def _valid_user (thing):
    return _valid (thing, 'uid', 'User', global_ids.USER_NULL)

@contextmanager
def _valid_session (thing):
    with _valid (thing, 'user', 'Session', global_ids.USER_SESS_NULL) as session:
        yield session
        session.last_access = CurrentDateTime()

@contextmanager
def _valid_userroles (thing):
    with _valid_user (thing) as user:
        if user.roles is None or len(user.roles)<1:
            raise FortressError (msg='User role list empty', id=global_ids.ROLE_LST_NULL)
        yield user.roles

@contextmanager
def _valid_perm (thing):
    with _valid (thing, 'obj_name', 'Permission', global_ids.PERM_NULL) as perm:
        if perm.op_name is None:
            raise FortressError (msg='Perm op name is None', id=global_ids.PERM_OPERATION_NM_NULL)
        yield perm

def create_session (user, is_trusted):
    with _valid_user (user):
        session = Session()
        if is_trusted is False:
            userdao.authenticate (User(uid=user.uid,password=user.password))
            session.is_authenticated = True
        entity = userdao.read (user)
        session.user = entity
        with _valid_session (session):
            return session

def check_access (session, perm):
    with _valid_session (session):
        with _valid_perm (perm):
            return frozenset() < _join (session.user.roles.keys(),entity.roles.keys())

def _entity_role_set (roles):
    return frozenset (map (lambda r:r.casefold(), roles))

def _join (uroles, proles):
    return _entity_role_set(uroles) & _entity_role_set(proles)

def is_user_in_role (session, role):
    with _valid_session (session):
        try:
            with _valid_userroles (session.user) as roles:
                return _rolename(role) in _entity_role_set (session.user.roles)
        except FortressError as f:
            return False

def _rolename(rolething):
    if isinstance(rolething,Role):
        return rolething.name.casefold()
    else:
        return str(rolething).casefold()

def add_active_role (session, role):
    with _valid_session (session):
        if is_user_in_role (session, role):
            raise FortressError (msg='add_active_role uid=' + session.user.uid + ', previously activated role=' + role, id=global_ids.URLE_ALREADY_ACTIVE)
        user = userdao.read(session.user)
        rn = _rolename(role)
        if rn in _entity_role_set(user.roles):
            session.user.roles[rn] = user.roles[rn]
        else:
            raise FortressError (msg='add_active_role uid=' + session.user.uid + ', has not been assigned role=' + role, id=global_ids.URLE_ASSIGN_NOT_EXIST)

def drop_active_role (session, role):
    with _valid_session (session):
        if not is_user_in_role (session, role):
            raise FortressError (msg='drop_active_role uid=' + session.user.uid + ', has not activated role=' + role, id=global_ids.URLE_NOT_ACTIVE)
        session.user.roles.pop(_rolename(role), None)

def session_roles (session):
    with _valid_session (session):
        try:
            with _valid_userroles (session.user) as roles:
                return roles
        except FortressError as f:
            return []

def session_perms (session):
    with _valid_session (session):
        try:
            with _valid_userroles (session.user):
                return permdao.search_on_roles(session.user.roles)
        except FortressError as f:
            return []
