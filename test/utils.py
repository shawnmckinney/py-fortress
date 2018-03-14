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

def print_thing (entity, label):
    print (label)
    for name in entity.__dict__:
        print ("\t{0}: {1}".format(name,entity.__dict__[name]))

def print_constraint (constraint, label):
        print_ln(label, 1)    
        print_ln('name=' + constraint.name, 2)
        print_ln('timeout=' + constraint.timeout, 2)
        print_ln('begin_time=' + constraint.begin_time, 2)
        print_ln('end_time=' + constraint.end_time, 2)
        print_ln('begin_date=' + constraint.begin_date, 2)
        print_ln('end_date=' + constraint.end_date, 2)
        print_ln('begin_lock_date=' + constraint.begin_lock_date, 2)
        print_ln('end_lock_date=' + constraint.end_lock_date, 2)
        print_ln('day_mask=' + constraint.day_mask, 2)


def print_user (entity, label):
        print_ln(label)
        print_ln('uid=' + str(entity.uid), 1)
        print_ln('dn=' + str(entity.dn), 1)
        print_ln('cn=' + str(entity.cn), 1)
        print_ln('sn=' + str(entity.sn), 1)
        print_ln('description=' + str(entity.description), 1)            
        print_ln('ou=' + str(entity.ou), 1)
        print_ln('internal_id=' + str(entity.internal_id), 1)
        print_ln('roles=' + str(entity.roles), 1)
        print_ln('pw_policy=' + str(entity.pw_policy), 1)                
        print_ln('display_name=' + str(entity.display_name), 1)        
        print_ln('employee_type=' + str(entity.employee_type), 1)
        print_ln('title=' + str(entity.title), 1)
        print_ln('phones=' + str(entity.phones), 1)
        print_ln('mobiles=' + str(entity.mobiles), 1)
        print_ln('emails=' + str(entity.emails), 1)        
        print_ln('reset=' + str(entity.reset), 1)
        print_ln('lockedTime=' + str(entity.locked_time), 1)
        print_ln('system=' + str(entity.system), 1)
        print_ln('props=' + str(entity.props), 1)        
        print_ln('department_number=' + str(entity.department_number), 1)
        print_ln('l=' + str(entity.l), 1)
        print_ln('physical_delivery_office_name=' + str(entity.physical_delivery_office_name), 1)
        print_ln('postal_code=' + str(entity.postal_code), 1)
        print_ln('room_number=' + str(entity.room_number), 1)
        print_constraint (entity.constraint, "User Constraint:")
        for idx, constraint in enumerate(entity.role_constraints) :
            print_constraint (constraint, "User-Role Constraint[" + str(idx+1) + "]:")
            
        print_ln("*************** " + label + " *******************")

    
def print_perm (entity, label):
        print_ln(label)
        print_ln('obj_name=' + str(entity.obj_name), 1)
        print_ln('op_name=' + str(entity.op_name), 1)
        print_ln('obj_id=' + str(entity.obj_id), 1)
        print_ln('description=' + str(entity.description), 1)            
        print_ln('internal_id=' + str(entity.internal_id), 1)        
        print_ln('abstract_name=' + str(entity.abstract_name), 1)
        print_ln('type=' + str(entity.type), 1)
        print_ln('users=' + str(entity.users), 1)
        print_ln('roles=' + str(entity.roles), 1)        
        print_ln('dn=' + str(entity.dn), 1)
        print_ln('props=' + str(entity.props), 1)
        print_ln("*************** " + label + " *******************")        
