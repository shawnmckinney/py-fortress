'''
Created on Mar 2, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from model import Session
from util.date import Date
from util.day import Day
from util.lockdate import LockDate
from util.time import Time
from util.current_date_time import CurrentDateTime
from ldap import permdao, userdao
from util.fortress_error import FortressError
from util.logger import logger
from util import global_ids
from util.global_ids import SUCCESS


validators = []
validators.append(Date())
validators.append(Day())
validators.append(LockDate())
validators.append(Time())

def create_session (user, is_trusted):
    """
    Perform user authentication User.password and role activations.
    This method must be called once per user prior to calling other methods within this module. 
    The successful result is Session that contains target user's RBAC User.roles.
    
    This API will...

    * authenticate user password if trusted == false.
    * evaluate temporal Constraint(s) on User and UserRoles.
    * process selective role activations into User RBAC Session User.roles.
    * return a Session containing Session.user, Session.user.roles
    
    required parameters:
    user.uid - maps to INetOrgPerson uid
    is_trusted - boolean, if 'True', authentication is skipped (password not checked)     
    """    
    __validate_user(user)
    session = Session()
    if is_trusted is False:
        # failure throws exception:
        userdao.authenticate(user)
        session.is_authenticated = True
    entity = userdao.read(user)    
    result = __validate_constraint(entity.constraint)
    if result is not SUCCESS:
        raise FortressError (msg='create_session constraint validation failed uid:' + entity.uid, id=result)
    __validate_role_constraints(entity)
    session.user = entity    
    return session


def check_access (session, perm):
    """
    Perform user RBAC authorization. 
    This function returns a Boolean value meaning whether the subject of a given session is allowed or not to perform a given operation on a given object. 
    The function is valid if and only if the session is a valid Fortress session, the object is a member of the OBJS data set, and the operation is a member of the OPS data set. 
    The session's subject has the permission to perform the operation on that object if and only if that permission is assigned to (at least) one of the session's active roles. 
    This implementation will verify the roles or userId correspond to the subject's active roles are registered in the object's access control list.
    
    required parameters:
    session - as returned from create_session api
    perm.obj_name - maps to already existing perm object    
    perm.op_name - maps to already existing op name    
        
    optional parameters:
    perm.obj_id    
    """        
    __validate(session)
    __validate_perm(perm)    
    result = False
    entity = permdao.read(perm)
    __validate_role_constraints(session.user)
    for role in session.user.roles:
        if any ( s.lower() == role.lower() for s in entity.roles ):        
            result = True
            break
    return result


def is_user_in_role (session, role):
    """
    
    required parameters:
    session - as returned from create_session api    
    role.name - maps to existing role     
    """        
    __validate(session)
    result = False
    __validate_role_constraints(session.user)
    if any ( s.lower() == role.lower() for s in session.user.roles ):
        result = True
    return result


def add_active_role (session, role):
    """
    This function adds a role as an active role of a session whose owner is a given user. 
    
    required parameters:
    session - as returned from create_session api    
    role.name - maps to existing role     
    """    
    __validate(session)    
    if any ( s.lower() == role.lower() for s in session.user.roles ):
        raise FortressError (msg='add_active_role uid=' + session.user.uid + ', previously activated role=' + role, id=global_ids.ROLE_ALREADY_ACTIVATED_ERROR)
    user = userdao.read(session.user)        
    for role_constraint in user.role_constraints:
        if role.lower() == role_constraint.name.lower():
            __activate_role(session.user, role_constraint)
    __validate_role_constraints(session.user)


def drop_active_role (session, role):
    """
    This function deletes a role from the active role set of a session owned by a given user. 
    The function is valid if and only if the user is a member of the USERS data set, the session object contains a valid Fortress session, 
    the session is owned by the user, and the role is an active role of that session.
    
    required parameters:
    session - as returned from create_session api    
    role.name - maps to existing role     
    """    
    __validate(session)
    found = False
    for role_constraint in session.user.role_constraints:        
        if role.lower() == role_constraint.name.lower():
            __deactivate_role(session.user, role_constraint)
            found = True            
    if not found:            
        raise FortressError (msg='drop_active_role uid=' + session.user.uid + ', has not activated role=' + role, id=global_ids.ROLE_NOT_ACTIVATED_ERROR)
    __validate_role_constraints(session.user)


def session_perms (session):
    """
    This function returns the permissions of the session, i.e., the permissions assigned to its authorized roles. 
    The function is valid if and only if the session is a valid Fortress session.

    required parameters:    
    session - as returned from create_session api    
    """    
    __validate(session)
    __validate_roles(session.user)    
    __validate_role_constraints(session.user)            
    return permdao.search_on_roles(session.user.roles)


def session_roles (session):
    """
    This function returns the active roles associated with a session. The function is valid if and only if the session is a valid Fortress session.

    required parameters:        
    session - as returned from create_session api    
    """    
    __validate(session)
    __validate_roles(session.user)    
    __validate_role_constraints(session.user)
    return session.user.role_constraints            


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
        raise FortressError ('User roles is None')
    elif len(user.roles) < 1:
        raise FortressError ('User roles is Empty')


def __validate_user(user):
    if user is None:
        raise FortressError ('User is None')
    elif user.uid is None:
        raise FortressError ('User uid is None')


def __validate_perm(perm):
    if perm is None:
        raise FortressError ('Perm is None')
    elif perm.obj_name is None:
        raise FortressError ('Perm object name is None')
    elif perm.op_name is None:
        raise FortressError ('Perm op name is None')


def __validate_role_constraints(user):
    for role_constraint in user.role_constraints:
        result = __validate_constraint(role_constraint)
        if result is not SUCCESS:
                logger.debug('validate_role_constraints deactivate user-role:' + user.uid + '.' + role_constraint.name)
                __deactivate_role(user, role_constraint)                

def __is_constraint(constraint):
    is_valid = True
    if constraint.raw is not None and not constraint.raw:
        is_valid = False
    return is_valid

def __validate_constraint(constraint):
    result = SUCCESS
    if __is_constraint(constraint):
        for validator in validators:
            result = validator.validate(constraint, CurrentDateTime())
            if result is not SUCCESS:
                logger.debug(validator.__class__.__name__ + ' validation failed:' + constraint.name )
                break
    return result