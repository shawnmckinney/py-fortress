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
from util.global_ids import SUCCESS

validators = []
validators.append(Date())
validators.append(Day())
validators.append(LockDate())
validators.append(Time())
# TODO addme:
#validators.append(TimeOut())

def create_session (user, is_trusted):
    session = Session()
    result = True
    if is_trusted is False:
        # will raise exception if fails:
        userdao.authenticate(user)
        session.is_authenticated = True
        
    entity = userdao.read(user)        
    result = __validate_constraint(entity.constraint)
    if result is not SUCCESS:
        raise FortressError ('User constraint validation failed uid=' + entity.uid, result)
    __validate_role_constraints(entity)
    session.user = entity    
    return session

def __validate_role_constraints(user):
    for role_constraint in user.role_constraints:
        result = __validate_constraint(role_constraint)
    if result is not SUCCESS:
            logger.debug('deactivate user-role: ' + user.uid + '.' + role_constraint.name)
            user.roles.remove(role_constraint.name)
            user.role_constraints.remove(role_constraint)


def __validate_constraint(constraint):
    result = SUCCESS
    for validator in validators:
        result = validator.validate(constraint, CurrentDateTime())
        if result is not SUCCESS:
            logger.debug(validator.__class__.__name__ + ' validation failed:' + constraint.name )
            break
    return result


def check_access (session, permission):
    result = False
    # TODO validate constraints here:
    
    entity = permdao.read(permission)
    
    # TODO check perm here:
    # for ever user-role in activation list... do
    
    return result


def is_user_in_role (session, role):
    result = False
    # TODO validate constraints here:
    
    # TODO check role here:
    # for ever user-role in activation list... do
    
    return result
