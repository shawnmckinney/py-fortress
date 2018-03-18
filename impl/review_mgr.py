'''
Created on Mar 18, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from ldap import permdao, userdao, roledao
from impl import utils


def read_user(entity):
    utils.validate_user(entity)
    return userdao.read(entity)

    
def find_users(entity):
    utils.validate_user(entity)
    return userdao.search(entity)

    
def read_role(entity):
    utils.validate_role(entity)
    return roledao.read(entity)

    
def find_roles(entity):
    utils.validate_role(entity)
    return roledao.search(entity)


def read_object(entity):
    utils.validate_perm_obj(entity)
    return permdao.read_obj(entity)

    
def find_objects(entity):
    utils.validate_perm_obj(entity)
    return permdao.search_objs(entity)

    
def read_perm(entity):
    utils.validate_perm(entity)
    return permdao.read(entity)

    
def find_perms(entity):
    utils.validate_perm(entity)
    return permdao.search(entity)


def assigned_users(entity):
    utils.validate_role(entity)
    return roledao.get_members(entity)
        
    
def assigned_roles(entity):
    utils.validate_user(entity)
    usr = userdao.read(entity)
    return usr.role_constraints


def perm_roles(entity):
    utils.validate_perm(entity)
    perm = permdao.read(entity)
    return perm.roles


def role_perms(entity):
    utils.validate_role(entity)
    return permdao.search_on_roles([entity.name])


def user_perms(entity):
    utils.validate_user(entity)
    usr = userdao.read(entity)    
    return permdao.search_on_roles(usr.roles)


def perm_users(entity):
    utils.validate_perm(entity)
    perm = permdao.read(entity)
    return userdao.search_on_roles(perm.roles)