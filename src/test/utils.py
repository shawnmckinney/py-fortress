'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from ..util import logger

def print_ln( ln, num=None ):
    if num is None:
        num = 0
    tabs = ''
    for x in range(0, num):
      tabs += '\t'        
    print( tabs + ln )    
    logger.debug( ( tabs + ln ) )    

def print_entity (entity, label, indent=None):
    if indent is None:
        indent = 1
    print_ln(label, indent-1)    
    for name in entity.__dict__:
        if name != 'password':
            value = entity.__dict__[name]
            if value:
                print_ln ("\t{0}: {1}".format(name,value), indent)

def print_user (entity, label):
        print_entity (entity, label, 1)
        if entity.constraint is not None:
            print_entity (entity.constraint, "User Constraint:", 2)
            
        if entity.role_constraints is not None:
            for idx, constraint in enumerate(entity.role_constraints) :
                #print_constraint (constraint, "User-Role Constraint[" + str(idx+1) + "]:")
                if constraint.name:
                    print_entity (constraint, "User-Role Constraint[" + str(idx+1) + "]:", 2)
        print_ln("*************** " + label + " *******************")
        
def print_role (entity, label):
        print_entity (entity, label, 1)
        if entity.constraint is not None and entity.constraint.name:        
            print_entity (entity.constraint, "Role Constraint:", 2)
        print_ln("*************** " + label + " *******************")
                