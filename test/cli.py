'''
Created on Mar 23, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''
import argparse
from argparse import ArgumentError
from model import PermObj, Perm, User, Role
from impl import admin_mgr, review_mgr
from test.utils import print_user, print_role, print_ln, print_entity
# entities =
USER = 'user'
ROLE = 'role'
PERM = 'perm'
OBJECT = 'object'
#operations =
ADD = 'add'
UPDATE = 'mod'
DELETE = 'del'
ASSIGN = 'assign'
DEASSIGN = 'deassign'
GRANT = 'grant'
REVOKE = 'revoke'
READ = 'read'
SEARCH = 'search'


def process(args):
    result = False
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
                        
                        
def load_entity (entity, args):
    for name in entity.__dict__:
        value = args.__dict__[name]
        if value:
            entity.__dict__[name] = value
            if name != 'password':
                print(name + '=' + value)
    return entity

    
def process_user(args):
    user = load_entity (User(), args)
    print(args.entity + ' ' + args.operation)    
    if args.operation == ADD:
        admin_mgr.add_user(user)
    elif args.operation == UPDATE:
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
    role = load_entity (Role(), args)
    print(args.entity + ' ' + args.operation)        
    if args.operation == ADD:
        admin_mgr.add_role(role)        
    elif args.operation == UPDATE:
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
        
        
def add_args (parser, entity):
    for name in entity.__dict__:
        try:
            parser.add_argument('--' + name)
        except ArgumentError as e:
            #ignore
            pass


parser = argparse.ArgumentParser(description='Process py-fortress commands.')
parser.add_argument('entity', metavar='entity', choices=[USER, ROLE, PERM, OBJECT], help='entity name')
parser.add_argument('operation', metavar='operand', choices=[ADD, UPDATE, DELETE, ASSIGN, DEASSIGN, GRANT, REVOKE, READ, SEARCH], help='operation name')
parser.add_argument('-r', '--role', dest='role', help='role name')
add_args(parser, Role())
add_args(parser, User())
add_args(parser, Perm())    
add_args(parser, PermObj())
args = parser.parse_args()
process(args)