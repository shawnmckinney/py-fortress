'''
@copyright: 2022 - Symas Corporation
'''
from rbac.ldap import permdao, userdao, roledao
from rbac.util import utils


def read_user(user):
    """
    Method returns matching User entity that is contained within the people container in the directory. 
    
    required parameters:
    user.uid - maps to INetOrgPerson uid  
    
    return:
    User   
    """    
    utils.validate_user(user)
    return userdao.read(user)

    
def find_users(user):
    """
    Return a list of type User of all users in the people container that match all or part of the User.userId field passed in User entity. 
    
    required parameters:
    user.uid - maps to existing user, can be partial with wildcard on end - *
    
    optional parameters:
    user.ou - maps to attribute assignment, can be partial with wildcard on end - *.
         
    return:
    User list   
    """    
    utils.validate_user(user)
    return userdao.search(user)

    
def read_role(role):
    """
    Method reads Role entity from the role container in directory. 
    
    required parameters:
    role.name - maps to existing role  
           
    return:
    Role   
    """    
    utils.validate_role(role)
    return roledao.read(role)

    
def find_roles(role):
    """
    Method will return a list of type Role matching all or part of Role name, Role.name.
    
    required parameters:
    role.name - maps to existing role.  May be partial name with wildcard on end - *. 
        
    return:
    Role list   
    """    
    utils.validate_role(role)
    return roledao.search(role)


def read_object(perm_obj):
    """
    Method reads permission object from perm container in directory. 
    
    required parameters:
    perm.obj_name - maps to existing perm object.   
         
    return:
    PermObj   
    """    
    utils.validate_perm_obj(perm_obj)
    return permdao.read_obj(perm_obj)

    
def find_objects(perm_obj):
    """
    Method returns a list of type PermObj that match the perm object search string. 
    
    required parameters:
    perm.obj_name - maps to existing perm object.  May be partial with wildcard on end - *.
            
    return:
    PermObj list   
    """    
    utils.validate_perm_obj(perm_obj)
    return permdao.search_objs(perm_obj)

    
def read_perm(perm):
    """
    This method returns a matching permission entity to caller. 
    
    required parameters:
    perm.obj_name - maps to already existing perm object    
    perm.op_name - maps to already existing op name
        
    optional parameters:
    perm.obj_id    
    
    return:
    Perm   
    """    
    utils.validate_perm(perm)
    return permdao.read(perm)

    
def find_perms(perm):
    """
    Method returns a list of type Permission that match the perm object search string. 
    
    required parameters:
    perm.obj_name - maps to already existing perm object.  May be partial name with wildcard on end - *.    
    perm.op_name - maps to already existing op name.  May be partial name with wildcard on end - *.
        
    optional parameters:
    perm.obj_id.  May be partial with wildcard.
        
    return:
    Perm list   
    """    
    utils.validate_perm(perm)
    return permdao.search(perm)


def assigned_users(role):
    """
    This function returns the set of users assigned to a given role. The function is valid if and only if the role is a member of the ROLES data set. 
    
    required parameters:
    role.name - maps to existing role 
        
    return:
    String list of uids   
    """    
    utils.validate_role(role)
    return roledao.get_members(role)
        
    
def assigned_roles(user):
    """
    This function returns the set of roles assigned to a given user. The function is valid if and only if the user is a member of the USERS data set.
    
    required parameters:
    user.uid - maps to existing user 
            
    return:
    Constraint list   
    """    
    utils.validate_user(user)
    usr = userdao.read(user)
    return usr.role_constraints


def perm_roles(perm):
    """
    Return a list of type String of all roles that have granted a particular permission. 
    
    required parameters:
    perm.obj_name - maps to already existing perm object    
    perm.op_name - maps to already existing op name
    
    optional parameters:
    perm.obj_id    
    
    return:
    String list of role names   
    """    
    utils.validate_perm(perm)
    out_perm = permdao.read(perm)
    return out_perm.roles


def role_perms(role):
    """
    This function returns the set of all permissions (op, obj), granted to or inherited by a given role. The function is valid if and only if the role is a member of the ROLES data set. 
    
    required parameters:
    role.name - maps to existing role  
           
    return:
    Perm list   
    """    
    utils.validate_role(role)
    return permdao.search_on_roles([role.name])


def user_perms(user):
    """
    This function returns the set of permissions a given user gets through his/her authorized roles. The function is valid if and only if the user is a member of the USERS data set. 
    
    required parameters:
    user.uid - maps to INetOrgPerson uid
         
    return:
    Perm list   
    """    
    utils.validate_user(user)
    usr = userdao.read(user)    
    return permdao.search_on_roles(usr.roles)


def perm_users(perm):
    """
    Return all users that have been granted a particular permission via their role assignments.
    
    required parameters:
    perm.obj_name - maps to already existing perm object    
    perm.op_name - maps to already existing op name
        
    optional parameters:
    perm.obj_id
        
    return:
    User list   
    """    
    utils.validate_perm(perm)
    out_perm = permdao.read(perm)
    return userdao.search_on_roles(out_perm.roles)