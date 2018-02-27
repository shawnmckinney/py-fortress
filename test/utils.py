'''
Created on Feb 24, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from model import User, Permission

def print_constraint (constraint, label):
        print('\t' + label)    
        print('\t\t' + 'name=' + constraint.name)
        print('\t\t' + 'timeout=' + constraint.timeout)
        print('\t\t' + 'begin_time=' + constraint.begin_time)
        print('\t\t' + 'end_time=' + constraint.end_time)
        print('\t\t' + 'begin_date=' + constraint.begin_date)
        print('\t\t' + 'end_date=' + constraint.end_date)
        print('\t\t' + 'begin_lock_date=' + constraint.begin_lock_date)
        print('\t\t' + 'end_lock_date=' + constraint.end_lock_date)
        print('\t\t' + 'day_mask=' + constraint.day_mask)

def print_user (entity, label):
        print(label)
        print('\t' + 'uid=' + str(entity.uid))
        print('\t' + 'dn=' + str(entity.dn))
        print('\t' + 'cn=' + str(entity.cn))
        print('\t' + 'sn=' + str(entity.sn))
        print('\t' + 'description=' + str(entity.description))            
        print('\t' + 'ou=' + str(entity.ou))
        print('\t' + 'internal_id=' + str(entity.internal_id))
        print('\t' + 'roles=' + str(entity.roles))
        print('\t' + 'pw_policy=' + str(entity.pw_policy))                
        print('\t' + 'display_name=' + str(entity.display_name))        
        print('\t' + 'employee_type=' + str(entity.employee_type))
        print('\t' + 'title=' + str(entity.title))
        print('\t' + 'phones=' + str(entity.phones))
        print('\t' + 'mobiles=' + str(entity.mobiles))
        print('\t' + 'emails=' + str(entity.emails))        
        print('\t' + 'reset=' + str(entity.reset))
        print('\t' + 'lockedTime=' + str(entity.locked_time))
        print('\t' + 'system=' + str(entity.system))
        print('\t' + 'props=' + str(entity.props))        
        print('\t' + 'department_number=' + str(entity.department_number))
        print('\t' + 'l=' + str(entity.l))
        print('\t' + 'physical_delivery_office_name=' + str(entity.physical_delivery_office_name))
        print('\t' + 'postal_code=' + str(entity.postal_code))
        print('\t' + 'room_number=' + str(entity.room_number))
        print_constraint (entity.constraint, "User Constraint:")
        for idx, constraint in enumerate(entity.roleConstraints) :
            print_constraint (constraint, "User-Role Constraint[" + str(idx+1) + "]:")
            
        print("*************** " + label + " *******************")

    
def print_perm (entity, label):
        print(label)
        print('\t' + 'obj_name=' + str(entity.obj_name))
        print('\t' + 'op_name=' + str(entity.op_name))
        print('\t' + 'obj_id=' + str(entity.obj_id))
        print('\t' + 'description=' + str(entity.description))            
        print('\t' + 'internal_id=' + str(entity.internal_id))        
        print('\t' + 'abstract_name=' + str(entity.abstract_name))
        print('\t' + 'type=' + str(entity.type))
        print('\t' + 'users=' + str(entity.users))
        print('\t' + 'roles=' + str(entity.roles))        
        print('\t' + 'dn=' + str(entity.dn))
        print('\t' + 'props=' + str(entity.props))