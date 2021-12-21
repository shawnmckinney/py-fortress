'''
@copyright: 2022 - Symas Corporation
'''

from rbac.ldap import permdao, userdao, roledao
from rbac.util import global_ids, utils
from rbac.util.fortress_error import RbacError
from rbac.model import Perm, User, Role
from rbac.util import logger

def add_user(user):
    """
    This command creates a new RBAC user. The command is valid only if the new user is not already a member of the USERS data set. 
    The USER data set is updated. The new user does not own any session at the time of its creation.
    
    required parameters:
    user.uid - maps to INetOrgPerson uid
         
    optional parameters Temporal constraints may be associated with ftUserAttrs aux object class based on:
    user.constraint.name - just a label, i.e. uid
    user.constraint.timeout - 99 - set the integer timeout that contains max time (in minutes) that entity may remain inactive.    
    user.constraint.begin_date - YYYYMMDD - determines date when user may be activated.
    user.constraint.end_date - YYMMDD - indicates latest date user may be activated.
    user.constraint.begin_lock_date - YYYYMMDD - determines beginning of enforced inactive status
    user.constraint.end_lock_date - YYMMDD - determines end of enforced inactive status.
    user.constraint.begin_time - HHMM - determines begin hour user may be activated.
    user.constraint.end_time -  user.role.constraints.end_time -  HHMM - determines end hour user may be activated.
    user.constraint.day_mask - 1234567, 1 = Sunday, 2 = Monday, etc - specifies which day of week user may be activated.
    user.props - multi-occurring name:value pairs
    user.pw_policy - slapd pwpolicy
    
    standard iNetOrgPerson attrs, more info here: https://tools.ietf.org/html/rfc2798:
    user.ou
    user.cn
    user.sn
    user.dn
    user.description
    user.display_name
    user.employee_type
    user.title
    user.phones
    user.mobiles
    user.emails
    user.department_number
    user.l
    user.physical_delivery_office_name
    user.postal_code
    user.room_number                                     
    """    
    utils.validate_user(user)
    return userdao.create(user)

    
def update_user(user):
    """
    This method performs an update on User entity in directory. Prior to making this call the entity must exist in directory.
         
    required parameters:
    user.uid - maps to INetOrgPerson uid     
    optional parameters Temporal constraints may be associated with ftUserAttrs aux object class based on:
    user.constraint.name - just a label, i.e. uid
    user.constraint.timeout - 99 - set the integer timeout that contains max time (in minutes) that entity may remain inactive.    
    user.constraint.begin_date - YYYYMMDD - determines date when user may be activated.
    user.constraint.end_date - YYMMDD - indicates latest date user may be activated.
    user.constraint.begin_lock_date - YYYYMMDD - determines beginning of enforced inactive status
    user.constraint.end_lock_date - YYMMDD - determines end of enforced inactive status.
    user.constraint.begin_time - HHMM - determines begin hour user may be activated.
    user.constraint.end_time -  user.role.constraints.end_time -  HHMM - determines end hour user may be activated.
    user.constraint.day_mask - 1234567, 1 = Sunday, 2 = Monday, etc - specifies which day of week user may be activated.
    user.props - multi-occurring name:value pairs
    user.pw_policy - slapd pwpolicy
    standard iNetOrgPerson attrs, more info here: https://tools.ietf.org/html/rfc2798
    user.ou
    user.cn
    user.sn
    user.dn
    user.description
    user.display_name
    user.employee_type
    user.title
    user.phones
    user.mobiles
    user.emails
    user.department_number
    user.l
    user.physical_delivery_office_name
    user.postal_code
    user.room_number                                     
    """    
    utils.validate_user(user)
    return userdao.update(user)

    
def delete_user(user):
    """
    This command deletes an existing user from the RBAC database. The command is valid if and only if the user to be deleted is a member of the USERS data set. 
    The USERS and UA data sets and the assigned_users function are updated. This method performs a "hard" delete. 
    It completely removes all data associated with this user from the directory. 
    User entity must exist in directory prior to making this call else exception will be thrown.
    
    required parameters:
    user.uid - maps to INetOrgPerson uid     
    """    
    utils.validate_user(user)
    # get the user's role assignments from its entry.
    out_user = userdao.read(user)
    # it's needed to remove the user membership from associated role entries.    
    for role_nm in out_user.roles:
        try:
            roledao.remove_member(Role(name=role_nm), user.uid)
            logger.info('admin.delete_user:' + user.uid + ', removed as member of role:' + role_nm)
        except RbacError as e:
            if e.id != global_ids.URLE_ASSIGN_NOT_EXIST:
                raise RbacError(msg=e.msg, id=e.id)
            else:
                logger.warn('admin.delete_user:' + user.uid + ', is not occupant of role:' + role_nm)
            
    # now remove the user entry:
    return userdao.delete(user)

            
def add_role(role):
    """
    This command creates a new role. The command is valid if and only if the new role is not already a member of the ROLES data set. 
    The ROLES data set is updated. Initially, no user or permission is assigned to the new role.
         
    required parameters:
    role.name - maps to INetOrgPerson uid
    
    optional parameters Temporal constraints may be associated with ftUserAttrs aux object class based on:
    role.props - multi-occurring name:value pairs
    role.description

    role.constraint.timeout - 99 - set the integer timeout that contains max time (in minutes) that entity may remain inactive.        
    role.constraint.beginDate - YYYYMMDD - determines date when role may be activated.
    role.constraint.endDate - YYMMDD - indicates latest date role may be activated.
    role.constraint.beginLockDate - YYYYMMDD - determines beginning of enforced inactive status
    role.constraint.endLockDate - YYMMDD - determines end of enforced inactive status.
    role.constraint.beginTime - HHMM - determines begin hour role may be activated in user's session.
    role.constraint.endTime - HHMM - determines end hour role may be activated in user's session.*
    role.constraint.dayMask - 1234567, 1 = Sunday, 2 = Monday, etc - specifies which day of week role may be activated.
    """    
    utils.validate_role(role)
    return roledao.create(role)

    
def update_role(role):
    """
    Method will update a Role entity in the directory. The role must exist in role container prior to this call. 
    
    required parameters:
    role.name - maps to INetOrgPerson uid
         
    optional parameters Temporal constraints may be associated with ftUserAttrs aux object class based on:
    role.props - multi-occurring name:value pairs
    role.description
    
    role.constraint.timeout - 99 - set the integer timeout that contains max time (in minutes) that entity may remain inactive.    
    role.constraint.beginDate - YYYYMMDD - determines date when role may be activated.
    role.constraint.endDate - YYMMDD - indicates latest date role may be activated.
    role.constraint.beginLockDate - YYYYMMDD - determines beginning of enforced inactive status
    role.constraint.endLockDate - YYMMDD - determines end of enforced inactive status.
    role.constraint.beginTime - HHMM - determines begin hour role may be activated in user's session.
    role.constraint.endTime - HHMM - determines end hour role may be activated in user's session.*
    role.constraint.dayMask - 1234567, 1 = Sunday, 2 = Monday, etc - specifies which day of week role may be activated.
    """    
    utils.validate_role(role)
    return roledao.update(role)

    
def delete_role(role):
    """
    This command deletes an existing role from the RBAC database. The command is valid if and only if the role to be deleted is a member of the ROLES data set. 
    This command will also deassign role from all users.
     
    required parameters:
    role.name - maps to INetOrgPerson uid     
    """    
    utils.validate_role(role)
    
    # if role has members, deassign all.
    members, constraint = roledao.get_members_constraint (role)
    for member in members:
        try:
            userdao.deassign(User(uid=member), constraint)
            logger.info('admin.delete_role:' + role.name + ', remove assign for user:' + member)
        except RbacError as e:
            if e.id != global_ids.URLE_ASSIGN_NOT_EXIST:
                raise RbacError(msg=e.msg, id=e.id)
            else:
                logger.warn('admin.delete_role:' + role.name + ', assign not exist for user:' + member)
            
    # if role is assigned to perms (i.e. granted), remove them as well.
    perms = permdao.search_on_roles([role.name])
    for perm in perms:
        permdao.revoke(perm, role)
        logger.info('admin.delete_role:' + role.name + ', remove grant for perm obj_name:' + perm.obj_name + ', op_name:' + perm.op_name)
    
    # now remove the role entry.                
    return roledao.delete(role)

                        
def add_perm(perm):
    """
    This method will add permission operation to an existing permission object which resides under ou=Permissions,ou=RBAC,dc=yourHostName,dc=com container in directory information tree. 
    The perm operation entity may have Role or User associations. The target Permission must not exist prior to calling. 
    A Fortress Permission instance exists in a hierarchical, one-many relationship between its parent and itself as stored in ldap tree: (PermObj*->Permission).
    
    required parameters:
    perm.obj_name - maps to already existing perm object    
    perm.op_name - accepts an arbitrary name for an operation that maps to runtime process.
        
    optional parameters:
    perm.obj_id - object identifier
    perm.props - multi-occurring property key and values are separated with a ':'. e.g. mykey1:myvalue1
    perm.type - any safe text
    perm.description - any safe text        
    """    
    utils.validate_perm(perm)
    return permdao.create(perm)

    
def update_perm(perm):
    """
    This method will update permission operation pre-existing in target directory under ou=Permissions,ou=RBAC,dc=yourHostName,dc=com container in directory information tree. 
    The perm operation entity may also contain Role or User associations to add or remove using this function. 
    The perm operation must exist before making this call. Only non-null attributes will be updated.

    required parameters:
    perm.obj_name - maps to already existing perm object    
    perm.op_name - maps to already existing op name
        
    optional parameters:
    perm.obj_id - object identifier
    perm.props - multi-occurring property key and values are separated with a ':'. e.g. mykey1:myvalue1
    perm.type - any safe text
    perm.description - any safe text                
    """    
    utils.validate_perm(perm)
    return permdao.update(perm)

    
def delete_perm(perm):
    """
    This method will remove permission operation entity from permission object. A Fortress permission is (object->operation). The perm operation must exist before making this call.
    
    required parameters:
    perm.obj_name - maps to already existing perm object    
    perm.op_name - maps to already existing op name
                
    optional parameters:
    perm.obj_id    
    """    
    utils.validate_perm(perm)
    return permdao.delete(perm)

                                                
def add_object(perm_obj):
    """
    This method will add permission object to perms container in directory. The perm object must not exist before making this call. 
    A PermObj instance exists in a hierarchical, one-many relationship between itself and children as stored in ldap tree: (PermObj*->Permission).
    
    required parameters:
    perm.obj_name - maps to arbitrary name of system resource.
            
    optional parameters
    perm_obj.description - any safe text
    perm_obj.type - contains any safe text
    perm_obj.props * - multi-occurring property key and values are separated with a ':'. e.g. mykey1:myvalue1
    """    
    utils.validate_perm_obj(perm_obj)
    return permdao.create_obj(perm_obj)

    
def update_object(perm_obj):
    """
    This method will update permission object in perms container in directory. 
    The perm object must exist before making this call. 
    A PermObj instance exists in a hierarchical, one-many relationship between itself and children as stored in ldap tree: (PermObj*->Permission).
        
    required parameters:
    perm.obj_name - maps to existing perm object.
            
    optional parameters
    perm_obj.description - any safe text
    perm_obj.type - contains any safe text
    perm_obj.props * - multi-occurring property key and values are separated with a ':'. e.g. mykey1:myvalue1
    """    
    utils.validate_perm_obj(perm_obj)
    return permdao.update_obj(perm_obj)

    
def delete_object(perm_obj):
    """
    This method will remove permission object to perms container in directory. This method will also remove in associated permissions that are attached to this object.
    
    required parameters:
    perm.obj_name - maps to existing perm object.        
    """    
    utils.validate_perm_obj(perm_obj)
    try:
        permdao.delete_obj(perm_obj)
    except RbacError as e:
        # if entry has children.
        if e.id == global_ids.PERM_OBJECT_DELETE_FAILED_NONLEAF:
            logger.warn('admin.delete_object non-leaf, obj_name:' + perm_obj.obj_name)
            # remove all of them.
            pList = permdao.search(Perm(obj_name=perm_obj.obj_name, op_name='*'))
            for perm in pList:
                permdao.delete(perm)
                logger.warn('admin.delete_object child obj_name:' + perm.obj_name + ', op_name:' + perm.op_name)
                
            # now try to remove this node once again
            permdao.delete_obj(perm_obj)
            logger.warn('admin.delete_object success after retry, obj_name:' + perm.obj_name)
        else:
            # can't handle this error so rethrow.
            raise RbacError(msg=e.msg, id=e.id)
    return


def assign(user, role):
    """
    This command assigns a user to a role.

    The command is valid if and only if:
        The user is a member of the USERS data set
        The role is a member of the ROLES data set
        The user is not already assigned to the role

    required parameters:
    user.uid - existing user.        
    role.name - existing role.    
    """    
    utils.validate_user(user)
    utils.validate_role(role)
    entity = roledao.read(role)
    # LDAP doesn't do well with sub-string indexes which is why the role assignments are stored within two separate multi-occurring attributes on the user entry -- roles' and 'role_constraints'.
    # The first, is a set of role names (only), and will be indexed for fast search.
    # the second, is a set of delimited strings containing the role name (once again) plus its associated temporal values. 
    userdao.assign(user, entity.constraint)
    
    # Fortress user-role assignments also keep member association on the role itself. 
    # The rationale for these assignments also stored on role is two-fold:
    # 1. works with traditional LDAP group-based authZ mechanisms
    # 2. makes role-users search query more efficient, as its stored on single entry.     
    roledao.add_member(entity, user.uid)

                                                                                                
def deassign(user, role):
    """
    This command deletes the assignment of the User from the Role entities. 
    The command is valid if and only if the user is a member of the USERS data set, the role is a member of the ROLES data set, 
    and the user is assigned to the role. Any sessions that currently have this role activated will not be effected. 
    Successful completion includes:
    User entity in USER data set has role assignment removed.
    Role entity in ROLE data set has userId removed as role occupant.
    
    required parameters:
    user.uid - existing user.        
    role.name - existing role.        
    """    
    utils.validate_user(user)
    utils.validate_role(role)
    out_user = userdao.read(user)
    for constraint in out_user.role_constraints:
        if constraint.name == role.name:
            found = True
            userdao.deassign(user, constraint)
            try:
                roledao.remove_member(role, user.uid)
            except RbacError as e:
                if e.id != global_ids.URLE_ASSIGN_NOT_EXIST:
                    raise RbacError(msg=e.msg, id=e.id)
                else:
                    logger.warn('admin.deassign remove member failed because not occupant. user:' + user.uid + ', role:' + role.name)
    if not found:
        raise RbacError(msg='Role deassign failed constraint not found', id=global_ids.URLE_DEASSIGN_FAILED)
        
            
def grant(perm, role):
    """
    This method will add permission operation to an existing permission object which resides under ou=Permissions,ou=RBAC,dc=yourHostName,dc=com container in directory information tree. 
    The perm operation entity may have Role or User associations. The target Permission must not exist prior to calling. 
    A Fortress Permission instance exists in a hierarchical, one-many relationship between its parent and itself as stored in ldap tree: (PermObj*->Permission).
        
    required parameters:
    perm.obj_name - existing perm obj.
    perm.obj_name - existing perm op.                
    role.name - existing role.

    optional parameters:
    perm.obj_id - object identifier
    """    
    utils.validate_role(role)
    utils.validate_perm(perm)
    return permdao.grant(perm, role)

                                                                                                
def revoke(perm, role):
    """
    This command revokes the permission to perform an operation on an object from the set of permissions assigned to a role. 
    The command is implemented by setting the access control list of the object involved. 
    The command is valid if and only if the pair (operation, object) represents a permission, the role is a member of the ROLES data set, and the permission is assigned to that role.
    
    required parameters:
    perm.obj_name - existing perm obj.
    perm.obj_name - existing perm op.                
    role.name - existing role.
        
    optional parameters:
    perm.obj_id - object identifier
    """    
    utils.validate_role(role)
    utils.validate_perm(perm)
    return permdao.revoke(perm, role)
                                                                                                                                                                         