'''
Created on Mar 18, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from ldap import permdao, userdao, roledao
from impl import utils


def add_user(user):
    utils.validate_user(user)
    return userdao.create(user)

    
def update_user(user):
    utils.validate_user(user)
    return userdao.create(user)

    
def delete_user(user):
    utils.validate_user(user)
    return userdao.delete(user)

            
def add_role(role):
    utils.validate_role(role)
    return roledao.create(role)

    
def update_role(role):
    utils.validate_role(role)
    return roledao.create(role)

    
def delete_role(role):
    utils.validate_role(role)
    return roledao.delete(role)

                        
def add_perm(perm):
    utils.validate_perm(perm)
    return permdao.create(perm)

    
def update_perm(perm):
    utils.validate_perm(perm)
    return permdao.create(perm)

    
def delete_perm(perm):
    utils.validate_perm(perm)
    return permdao.delete(perm)

                                                
def add_object(perm_obj):
    utils.validate_perm_obj(perm_obj)
    return permdao.create_obj(perm_obj)

    
def update_object(perm_obj):
    utils.validate_perm_obj(perm_obj)
    return permdao.create_obj(perm_obj)

    
def delete_object(perm_obj):
    utils.validate_perm_obj(perm_obj)
    return permdao.delete_obj(perm_obj)


def assign(user, role):
    utils.validate_user(user)
    utils.validate_role(role)
    entity = roledao.read(role)
    userdao.assign(user, entity.constraint)
    roledao.add_member(entity, user.uid)

                                                                                                
def deassign(user, role):
    utils.validate_user(user)
    utils.validate_role(role)
    entity = roledao.read(role)
    userdao.deassign(user, entity.constraint)
    roledao.remove_member(entity, user.uid)


def grant(perm, role):
    utils.validate_role(role)
    utils.validate_perm(perm)
    return permdao.grant(perm, role)

                                                                                                
def revoke(perm, role):
    utils.validate_role(role)
    utils.validate_perm(perm)
    return permdao.revoke(perm, role)
                                                                                                                                                                         