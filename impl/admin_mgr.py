'''
Created on Mar 18, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from ldap import permdao, userdao, roledao
from impl.fortress_error import FortressError
from util.logger import logger
from util import global_ids
from impl import utils


def add_user(entity):
    utils.validate_user(entity)
    return userdao.create(entity)

    
def update_user(entity):
    utils.validate_user(entity)
    return userdao.create(entity)

    
def delete_user(entity):
    utils.validate_user(entity)
    return userdao.delete(entity)

            
def add_role(entity):
    utils.validate_role(entity)
    return roledao.create(entity)

    
def update_role(entity):
    utils.validate_role(entity)
    return roledao.create(entity)

    
def delete_role(entity):
    utils.validate_role(entity)
    return roledao.delete(entity)

                        
def add_permission(entity):
    utils.validate_perm(entity)
    return permdao.create(entity)

    
def update_permission(entity):
    utils.validate_perm(entity)
    return permdao.create(entity)

    
def delete_permission(entity):
    utils.validate_perm(entity)
    return permdao.delete(entity)

                                                
def add_object(entity):
    utils.validate_perm_obj(entity)
    return permdao.create_obj(entity)

    
def update_object(entity):
    utils.validate_perm_obj(entity)
    return permdao.create_obj(entity)

    
def delete_object(entity):
    utils.validate_perm_obj(entity)
    return permdao.delete_obj(entity)


def assign(user, role):
    utils.validate_user(user)
    utils.validate_role(role)
    entity = roledao.read(role)
    return userdao.assign(user, entity.constraint)

                                                                                                
def deassign(user, role):
    utils.validate_user(user)
    utils.validate_role(role)
    entity = roledao.read(role)
    return userdao.deassign(user, entity.constraint)


def grant(perm, role):
    utils.validate_role(role)
    utils.validate_perm(perm)
    return permdao.grant(perm, role)

                                                                                                
def revoke(perm, role):
    utils.validate_role(role)
    utils.validate_perm(perm)
    return permdao.revoke(perm, role)
                                                                                                                                                                         