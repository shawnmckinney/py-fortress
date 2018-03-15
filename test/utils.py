'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from model import User, Permission
from util.logger import logger

def print_ln( ln, num=None ):
    if num is None:
        num = 0
    
    tabs = ''
    for x in range(0, num):
      tabs += '\t'        
    print( tabs + ln )    
    logger.debug( ( tabs + ln ) )    

def print_entity (entity, label, indent):
    print_ln(label, indent-1)    
    for name in entity.__dict__:
        print_ln ("\t{0}: {1}".format(name,entity.__dict__[name]), indent)

def print_user (entity, label):
        print_entity (entity, label, 1)
        print_entity (entity.constraint, "User Constraint:", 2)
        for idx, constraint in enumerate(entity.role_constraints) :
            #print_constraint (constraint, "User-Role Constraint[" + str(idx+1) + "]:")
            print_entity (constraint, "User-Role Constraint[" + str(idx+1) + "]:", 2)
        print_ln("*************** " + label + " *******************")
        