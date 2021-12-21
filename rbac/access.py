'''
@copyright: 2022 - Symas Corporation
'''

from rbac.model import Session
from rbac.util import Date, Day, LockDate, Time, TimeOut, CurrentDateTime
from rbac.ldap import userdao, permdao
from rbac.util.fortress_error import RbacError
from rbac.util import logger, global_ids, SUCCESS


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
    
    return:
    Session     
    """    
    __validate_user(user)
    session = Session()
    if is_trusted is False:
        # failure throws exception:
        userdao.authenticate(user)
        session.is_authenticated = True
    entity = userdao.read(user)
    session.user = entity            
    __validate_user_constraint(session, 'create_session')
    __validate_role_constraints(session)
    __refresh(session)
    return session


def check_access (session, perm):
    """
    Perform user RBAC authorization. 
    This function returns a Boolean value meaning whether the subject of a given session is allowed or not to perform a given operation on a given object. 
    The function is valid if and only if the session is a valid Fortress session,
    the object is a member of the OBJS data set, and the operation is a member of the OPS data set.
    The session's subject has the permission to perform the operation on that object if and only if that permission is assigned to (at least) one of the session's active roles.
    This implementation will verify the roles or userId correspond to the subject's active roles are registered in the object's access control list.
    
    required parameters:
    session - as returned from create_session api
    perm.obj_name - maps to already existing perm object    
    perm.op_name - maps to already existing op name    
        
    optional parameters:
    perm.obj_id    
    
    return:
    boolean True if allowed; False otherwise     
    """        
    __validate(session)
    __validate_perm(perm)    
    __validate_user_constraint(session, 'check_access')
    __validate_role_constraints(session)    
    result = False
    entity = permdao.read(perm)
    for role in session.user.roles:
        if __is_role_found(role, entity.roles):        
            result = True
            break
    __refresh(session)
    return result


def is_user_in_role (session, role):
    """
    This function returns a BOOLEAN value whether subject has the specified role contained within their session.
         
    required parameters:
    session - as returned from create_session api    
    role.name - maps to existing role     
    
    return:
    boolean True if allowed; False otherwise         
    """        
    __validate(session)
    __validate_user_constraint(session, 'is_user_in_role')    
    result = False
    __validate_role_constraints(session)
    if __is_role_found(role, session.user.roles):
        result = True
    __refresh(session)
    return result


def add_active_role (session, role):
    """
    This function adds a role as an active role of a session whose owner is a given user. 
    
    required parameters:
    session - as returned from create_session api    
    role.name - maps to existing role     
    
    return:
    None     
    """    
    __validate(session) 
    __validate_user_constraint(session, 'add_active_role')   
    if any ( s.lower() == role.lower() for s in session.user.roles ):
        raise RbacError (msg='add_active_role uid=' + session.user.uid + ', previously activated role=' + role, id=global_ids.URLE_ALREADY_ACTIVE)
    user = userdao.read(session.user)        
    constraint = __find_role_constraint(role, user.role_constraints)
    if constraint is not None:
       __activate_role(session.user, constraint)
    else:
        raise RbacError (msg='add_active_role uid=' + session.user.uid + ', has not been assigned role=' + role, id=global_ids.URLE_ASSIGN_NOT_EXIST)
    __validate_role_constraints(session)
    __refresh(session)


def drop_active_role (session, role):
    """
    This function deletes a role from the active role set of a session owned by a given user. 
    The function is valid if and only if the user is a member of the USERS data set, the session object contains a valid Fortress session, 
    the session is owned by the user, and the role is an active role of that session.
    
    required parameters:
    session - as returned from create_session api    
    role.name - maps to existing role     
    
    return:
    None     
    """    
    __validate(session)
    __validate_user_constraint(session, 'drop_active_role')
    constraint = __find_role_constraint(role, session.user.role_constraints)
    if constraint is not None:
        __deactivate_role(session.user, constraint)
    else:
        raise RbacError (msg='drop_active_role uid=' + session.user.uid + ', has not activated role=' + role, id=global_ids.URLE_NOT_ACTIVE)
    __validate_role_constraints(session)
    __refresh(session)


def session_roles (session):
    """
    This function returns the active roles associated with a session. The function is valid if and only if the session is a valid Fortress session.

    required parameters:        
    session - as returned from create_session api    
    
    return:
    Constraint list     
    """    
    __validate(session)
    __validate_user_constraint(session, 'session_roles')
    __validate_roles(session.user)    
    __validate_role_constraints(session)
    __refresh(session)
    return session.user.role_constraints            


def session_perms (session):
    """
    This function returns the permissions of the session, i.e., the permissions assigned to its authorized roles. 
    The function is valid if and only if the session is a valid Fortress session.

    required parameters:    
    session - as returned from create_session api    
    
    return:
    Perm list     
    """    
    __validate(session)
    __validate_user_constraint(session, 'session_perms')
    __validate_roles(session.user)    
    __validate_role_constraints(session)
    __refresh(session)            
    return permdao.search_on_roles(session.user.roles)


def __activate_role(user, role_constraint):
    user.roles.append(role_constraint.name)
    user.role_constraints.append(role_constraint)


def __deactivate_role(user, role_constraint):
    user.roles.remove(role_constraint.name)
    user.role_constraints.remove(role_constraint)


def __refresh(session):
    session.last_access = CurrentDateTime()            


def __validate(session):
    if session is None:
        raise RbacError (msg='Session is None', id=global_ids.USER_SESS_NULL)
    elif session.user is None:
        raise RbacError (msg='Session has no user', id=global_ids.USER_SESS_NULL)


def __validate_roles(user):
    if user.roles is None:
        raise RbacError (msg='User roles is None', id=global_ids.ROLE_LST_NULL)
    elif len(user.roles) < 1:
        raise RbacError (msg='User roles is Empty', id=global_ids.ROLE_LST_NULL)


def __validate_user(user):
    if user is None:
        raise RbacError (msg='User is None', id=global_ids.USER_NULL)
    elif user.uid is None:
        raise RbacError (msg='User uid is None', id=global_ids.USER_ID_NULL)


def __validate_perm(perm):
    if perm is None:
        raise RbacError (msg='Perm is None', id=global_ids.PERM_NULL)
    elif perm.obj_name is None:
        raise RbacError (msg='Perm object name is None', id=global_ids.PERM_OBJECT_NM_NULL)
    elif perm.op_name is None:
        raise RbacError (msg='Perm op name is None', id=global_ids.PERM_OPERATION_NM_NULL)


def __validate_role_constraints(session):
    for role_constraint in session.user.role_constraints:
        result = __validate_role_constraint(session, role_constraint)
        if result is not SUCCESS:
                logger.debug('validate_role_constraints deactivate user-role:' + session.user.uid + '.' + role_constraint.name + ', result=' + str(result))
                __deactivate_role(session.user, role_constraint)                


def __is_constraint(constraint):
    is_valid = True
    if constraint.raw is not None and not constraint.raw:
        is_valid = False
    return is_valid


def __validate_user_constraint(session, op):
    result = SUCCESS
    if __is_constraint(session.user.constraint):
        for validator in validators:
            result = validator.validate(session.user.constraint, CurrentDateTime(), session)
            if result is not SUCCESS:
                logger.debug(validator.__class__.__name__ + ' validation failed:' + session.user.constraint.name + ', result=' + str(result))
                raise RbacError (msg=op + ' constraint validation failed uid:' + session.user.uid, id=result)
    return result


def __validate_role_constraint(session, constraint):
    result = SUCCESS
    if __is_constraint(constraint):
        for validator in validators:
            result = validator.validate(constraint, CurrentDateTime(), session)
            if result is not SUCCESS:
                logger.debug(validator.__class__.__name__ + ' validation failed:' + constraint.name + ', uid=' + session.user.uid + ', result=' + str(result))
                break
    return result


def __is_role_found(role, roles):
    result = False
    if any ( s.lower() == role.lower() for s in roles ):        
        result = True
    return result


def __find_role_constraint(role, role_constraints):
    result = None    
    for role_constraint in role_constraints:
        if role.lower() == role_constraint.name.lower():
            result = role_constraint
    return result


# Initialize the constraint validators:
validators = []
validators.append(Date())
validators.append(Day())
validators.append(LockDate())
validators.append(Time())
validators.append(TimeOut())