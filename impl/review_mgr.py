'''
Created on Mar 18, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from ldap import permdao, userdao, roledao
from impl import utils


def read_user(user):
    utils.validate_user(user)
    return userdao.read(user)

    
def find_users(user):
    utils.validate_user(user)
    return userdao.search(user)

    
def read_role(role):
    utils.validate_role(role)
    return roledao.read(role)

    
def find_roles(role):
    utils.validate_role(role)
    return roledao.search(role)


def read_object(perm_obj):
    utils.validate_perm_obj(perm_obj)
    return permdao.read_obj(perm_obj)

    
def find_objects(perm_obj):
    utils.validate_perm_obj(perm_obj)
    return permdao.search_objs(perm_obj)

    
def read_perm(perm):
    utils.validate_perm(perm)
    return permdao.read(perm)

    
def find_perms(perm):
    utils.validate_perm(perm)
    return permdao.search(perm)


def assigned_users(role):
    utils.validate_role(role)
    return roledao.get_members(role)
        
    
def assigned_roles(user):
    utils.validate_user(user)
    usr = userdao.read(user)
    return usr.role_constraints


def perm_roles(perm):
    utils.validate_perm(perm)
    out_perm = permdao.read(perm)
    return out_perm.roles


def role_perms(role):
    utils.validate_role(role)
    return permdao.search_on_roles([role.name])


def user_perms(user):
    utils.validate_user(user)
    usr = userdao.read(user)    
    return permdao.search_on_roles(usr.roles)


def perm_users(perm):
    utils.validate_perm(perm)
    out_perm = permdao.read(perm)
    return userdao.search_on_roles(out_perm.roles)