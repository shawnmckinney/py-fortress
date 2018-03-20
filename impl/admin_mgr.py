'''
Created on Mar 18, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from ldap import permdao, userdao, roledao
from impl import utils
from util import global_ids
from util.fortress_error import FortressError
from model import Perm, User, Role

def add_user(user):
    """
    This command creates a new RBAC user. The command is valid only if the new user is not already a member of the USERS data set. 
    The USER data set is updated. The new user does not own any session at the time of its creation.
    
    required parameters:
    user.uid - maps to INetOrgPerson uid
         
    optional parameters Temporal constraints may be associated with ftUserAttrs aux object class based on:
    user.role_constraints.beginDate - YYYYMMDD - determines date when role may be activated.
    user.role_constraints.endDate - YYMMDD - indicates latest date role may be activated.
    user.role_constraints.beginLockDate - YYYYMMDD - determines beginning of enforced inactive status
    user.role_constraints.endLockDate - YYMMDD - determines end of enforced inactive status.
    user.role_constraints.beginTime - HHMM - determines begin hour role may be activated in user's session.
    user.role_constraints - HHMM - determines end hour role may be activated in user's session.*
    user.role_constraints - 1234567, 1 = Sunday, 2 = Monday, etc - specifies which day of week role may be activated.

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
    return userdao.create(user)

    
def update_user(user):
    """
    This method performs an update on User entity in directory. Prior to making this call the entity must exist in directory.
         
    required parameters:
    user.uid - maps to INetOrgPerson uid     
    optional parameters Temporal constraints may be associated with ftUserAttrs aux object class based on:
    user.role_constraints.beginDate - YYYYMMDD - determines date when role may be activated.
    user.role_constraints.endDate - YYMMDD - indicates latest date role may be activated.
    user.role_constraints.beginLockDate - YYYYMMDD - determines beginning of enforced inactive status
    user.role_constraints.endLockDate - YYMMDD - determines end of enforced inactive status.
    user.role_constraints.beginTime - HHMM - determines begin hour role may be activated in user's session.
    user.role_constraints - HHMM - determines end hour role may be activated in user's session.*
    user.role_constraints - 1234567, 1 = Sunday, 2 = Monday, etc - specifies which day of week role may be activated.

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
    return userdao.create(user)

    
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
    # first remove user's role memberships:
    out_user = userdao.read(user)
    for role in out_user.roles:
        try:
            roledao.remove_member(Role(name=role), user.uid)
        except FortressError as e:
            if e.id != global_ids.URLE_ASSIGN_NOT_EXIST:
                raise FortressError(msg=e.msg, id=e.id)
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
        except FortressError as e:
            if e.id != global_ids.URLE_ASSIGN_NOT_EXIST:
                raise FortressError(msg=e.msg, id=e.id)
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
    return permdao.create(perm)

    
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
    return permdao.create_obj(perm_obj)

    
def delete_object(perm_obj):
    """
    This method will remove permission object to perms container in directory. This method will also remove in associated permission objects that are attached to this object.
    
    required parameters:
    perm.obj_name - maps to existing perm object.        
    """    
    utils.validate_perm_obj(perm_obj)
    try:
        permdao.delete_obj(perm_obj)
    except FortressError as e:
        if e.id == global_ids.PERM_OBJECT_DELETE_FAILED_NONLEAF:
            pList = permdao.search(Perm(obj_name=perm_obj.obj_name, op_name='*'))
            for perm in pList:
                permdao.delete(perm)
            permdao.delete_obj(perm_obj)
        else:
            raise FortressError(msg=e.msg, id=e.id)
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
    userdao.assign(user, entity.constraint)
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
    entity = roledao.read(role)
    userdao.deassign(user, entity.constraint)
    try:
        roledao.remove_member(entity, user.uid)
    except FortressError as e:
        if e.id != global_ids.URLE_ASSIGN_NOT_EXIST:
            raise FortressError(msg=e.msg, id=e.id)
    


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
                                                                                                                                                                         