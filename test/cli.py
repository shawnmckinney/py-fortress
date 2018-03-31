'''
Created on Mar 23, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''
import argparse
from model import PermObj, Perm, User, Role, Constraint
from impl import admin_mgr, review_mgr
from test.utils import print_user, print_role, print_ln, print_entity
from util.fortress_error import FortressError
from test.cli_utils import (
    load_entity, add_args, USER, ROLE, PERM, OBJECT, ADD, 
    UPDATE, DELETE, ASSIGN, DEASSIGN, READ, SEARCH, GRANT, REVOKE
    )

def process(args):
    result = False
    try:
        if args.entity == USER:
            result = process_user(args)
        elif args.entity == ROLE:
            result = process_role(args)        
        elif args.entity == PERM:
            result = process_perm(args)                
        elif args.entity == OBJECT:
            result = process_object(args)
        else:
            print('process failed, invalid entity=' + args.entity)        
        if result:
            print('success')
    except FortressError as e:
        print('FortressError id=' + str(e.id) +', ' + e.msg)                        
                        

def process_user(args):
    user = load_entity(User(), args)
    print(args.entity + ' ' + args.operation)    
    if args.operation == ADD:
        constraint = load_entity(Constraint(), args)
        user.constraint = constraint
        admin_mgr.add_user(user)
    elif args.operation == UPDATE:
        constraint = load_entity(Constraint(), args)
        user.constraint = constraint
        admin_mgr.update_user(user)        
    elif args.operation == DELETE:
        admin_mgr.delete_user(user)        
    elif args.operation == ASSIGN:
        role_nm = args.role        
        print('role name=' + role_nm)
        admin_mgr.assign(user, Role(name=role_nm))                
    elif args.operation == DEASSIGN:
        role_nm = args.role        
        print('role name=' + role_nm)        
        admin_mgr.deassign(user, Role(name=role_nm))
    elif args.operation == READ:
        print_user(review_mgr.read_user(user), user.uid)
        pass
    elif args.operation == SEARCH:
        user.uid += '*'
        users = review_mgr.find_users(user)
        if len(users) > 0:
            for idx, usr in enumerate(users):
                print_user(usr, user.uid + ':' + str(idx))
        else:
            print_ln('No matching records found matching filter: ' + user.uid) 
    else:
        print('process_user failed, invalid operation=' + args.operation)
        return False
    return True                                

        
def process_role(args):
    role = load_entity(Role(), args)
    print(args.entity + ' ' + args.operation)        
    if args.operation == ADD:
        constraint = load_entity(Constraint(), args)
        role.constraint = constraint
        admin_mgr.add_role(role)        
    elif args.operation == UPDATE:
        constraint = load_entity(Constraint(), args)
        role.constraint = constraint
        admin_mgr.update_role(role)        
    elif args.operation == DELETE:
        admin_mgr.delete_role(role)
    elif args.operation == READ:
        print_role(review_mgr.read_role(role), role.name)
        pass
    elif args.operation == SEARCH:
        role.name += '*'
        roles = review_mgr.find_roles(role)
        if len(roles) > 0:
            for idx, rle in enumerate(roles):
                print_role(rle, role.name + ':' + str(idx))
        else:
            print_ln('No matching records found matching filter: ' + role.name) 
    else:
        print('process_role failed, invalid operation=' + args.operation)
        return False
    return True                                
       
        
def process_object(args):
    object = load_entity (PermObj(), args) 
    print(args.entity + ' ' + args.operation)   
    if args.operation == ADD:
        admin_mgr.add_object(object)        
    elif args.operation == UPDATE:
        admin_mgr.update_object(object)        
    elif args.operation == DELETE:
        admin_mgr.delete_object(object) 
    elif args.operation == READ:
        print_entity(review_mgr.read_object(object), object.obj_name)
        pass
    elif args.operation == SEARCH:
        object.obj_name += '*'
        objs = review_mgr.find_objects(object)
        if len(objs) > 0:
            for idx, obj in enumerate(objs):
                print_entity(obj, object.obj_name + ':' + str(idx))
        else:
            print_ln('No matching records found matching filter: ' + object.obj_name) 
    else:
        print('process_object failed, invalid operation=' + args.operation)
        return False
    return True                                
        
        
def process_perm(args):
    perm = load_entity (Perm(), args) 
    print(args.entity + ' ' + args.operation)       
    if args.operation == ADD:
        admin_mgr.add_perm(perm)        
    elif args.operation == UPDATE:
        admin_mgr.update_perm(perm)        
    elif args.operation == DELETE:
        admin_mgr.delete_perm(perm)        
    elif args.operation == GRANT:
        role_nm = args.role        
        print('role role_nm=' + role_nm)
        admin_mgr.grant(perm, Role(name=role_nm))                        
    elif args.operation == REVOKE:
        role_nm = args.role        
        print('role role_nm=' + role_nm)
        admin_mgr.revoke(perm, Role(name=role_nm))
    elif args.operation == READ:
        print_entity(review_mgr.read_perm(perm), perm.obj_name + '.' + perm.op_name)
        pass
    elif args.operation == SEARCH:
        role_nm = args.role
        userid = args.uid
        prms = []
        label = ''
        if userid:
            label = userid
            prms = review_mgr.user_perms(User(uid=userid))
        elif role_nm:
            label = role_nm
            prms = review_mgr.role_perms(Role(name=role_nm))
        else:        
            perm.obj_name += '*'
            if perm.op_name:
                perm.op_name += '*'
            else:
                perm.op_name = '*'
            label = perm.obj_name + '.' + perm.op_name            
            prms = review_mgr.find_perms(perm)
        if len(prms) > 0:
            for idx, prm in enumerate(prms):
                print_entity(prm, label + ':' + str(idx))
        else:
            print_ln('No matching records found matching filter: ' + label)                                 
    else:
        print('process_perm failed, invalid operation=' + args.operation)
        return False
    return True                                
        
        
parser = argparse.ArgumentParser(description='Process py-fortress admin and review commands.')
parser.add_argument('entity', metavar='entity', choices=[USER, ROLE, PERM, OBJECT], help='entity name')
parser.add_argument('operation', metavar='operand', choices=[ADD, UPDATE, DELETE, ASSIGN, DEASSIGN, GRANT, REVOKE, READ, SEARCH], help='operation name')
parser.add_argument('-r', '--role', dest='role', help='role name')
add_args(parser, Role())
add_args(parser, User())
add_args(parser, Perm())    
add_args(parser, PermObj())
add_args(parser, Constraint())
args = parser.parse_args()
process(args)