'''
Created on Mar 2, 2018

@author: smckinn
'''

from model import Session, User, Permission, Constraint
from util.validator import Validator
from util.date import Date
from util.day import Day
from util.lockdate import LockDate
from util.time import Time
from util.timeout import TimeOut
from util.current_date_time import CurrentDateTime
from ldap import permdao, userdao, LdapException, NotFound, NotUnique
from impl.fortress_error import FortressError
from util.logger import logger
from util import global_ids
from util.global_ids import SUCCESS


validators = []
validators.append(Date())
validators.append(Day())
validators.append(LockDate())
validators.append(Time())
# TODO addme:
#validators.append(TimeOut())

def create_session (user, is_trusted):
    __validate_user(user)
    session = Session()
    if is_trusted is False:
        # failure throws exception:
        userdao.authenticate(user)
        session.is_authenticated = True

    entity = userdao.read(user)    
    result = __validate_constraint(entity.constraint)
    if result is not SUCCESS:
        raise FortressError ('create_session constraint validation failed uid:' + entity.uid, result)
    
    __validate_role_constraints(entity)
    session.user = entity    
    return session


def check_access (session, permission):
    __validate(session)
    __validate_perm(permission)    
    result = False
    entity = permdao.read(permission)
    __validate_role_constraints(session.user)
    for role in session.user.roles:
        if any ( s.lower() == role.lower() for s in entity.roles ):        
            result = True
            break
        
    return result


def is_user_in_role (session, role):
    __validate(session)
    result = False
    __validate_role_constraints(session.user)
    if any ( s.lower() == role.lower() for s in session.user.roles ):
        result = True
                
    return result


def add_active_role (session, role):
    __validate(session)    
    if any ( s.lower() == role.lower() for s in session.user.roles ):
        logger.warn ('add_active_role uid=' + session.user.uid + ', previously activated role=' + role)
    
    user = userdao.read(session.user)
    for role_constraint in user.roles.role_constraints:
        if role.lower == role_constraint.name:
            __activate_role(session.user, role_constraint)
            
    __validate_role_constraints(session.user)


def drop_active_role (session, role):
    __validate(session)
    for role_constraint in session.user.role_constraints:
        if role.lower == role_constraint.name:
            __deactivate_role(session.user, role_constraint)
            found = True
            
    if not found:            
        logger.warn ('drop_active_role uid=' + session.user.uid + ', has not activated role=' + role)
                    
    __validate_role_constraints(session.user)


def session_permissions (session):
    __validate(session)
    __validate_role_constraints(session.user)    
    __validate_roles(session.user)        
    return permdao.search_on_roles(session.user.roles)


def session_roles (session):
    __validate(session)
    __validate_role_constraints(session.user)
    return session.role_constraints            


def __activate_role(user, role_constraint):
    user.roles.append(role_constraint.name)
    user.role_constraints.append(role_constraint)


def __deactivate_role(user, role_constraint):
    user.roles.remove(role_constraint.name)
    user.role_constraints.remove(role_constraint)


def __validate(session):
    if session is None:
        raise FortressError ('Session is None')
    elif session.user is None:
        raise FortressError ('Session has no user')


def __validate_roles(user):
    if user.roles is None:
        raise FortressError ('Session has no roles')


def __validate_user(user):
    if user is None:
        raise FortressError ('User is None')
    elif user.uid is None:
        raise FortressError ('User has no uid')


def __validate_perm(perm):
    if perm is None:
        raise FortressError ('Perm is None')
    elif perm.obj_name is None:
        raise FortressError ('Perm has no object name')
    elif perm.op_name is None:
        raise FortressError ('Perm has no op name')


def __validate_role_constraints(user):
    for role_constraint in user.role_constraints:
        result = __validate_constraint(role_constraint)
        if result is not SUCCESS:
                logger.debug('validate_role_constraints deactivate user-role:' + user.uid + '.' + role_constraint.name)
                __deactivate_role(user, role_constraint)                


def __validate_constraint(constraint):
    result = SUCCESS
    for validator in validators:
        result = validator.validate(constraint, CurrentDateTime())
        if result is not SUCCESS:
            logger.debug(validator.__class__.__name__ + ' validation failed:' + constraint.name )
            break
    return result