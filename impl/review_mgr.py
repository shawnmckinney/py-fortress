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

    
    

