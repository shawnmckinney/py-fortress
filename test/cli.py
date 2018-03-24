'''
Created on Mar 23, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''
import argparse
from argparse import ArgumentError
from model import PermObj, Perm, User, Role
from impl import admin_mgr

# entitys =
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
    if args.operation == ADD:
        print('process_user,add')
        admin_mgr.add_user(user)
    elif args.operation == UPDATE:
        print('process_user,update')
        admin_mgr.update_user(user)        
    elif args.operation == DELETE:
        print('process_user,delete')
        admin_mgr.delete_user(user)        
    elif args.operation == ASSIGN:
        name = args.role        
        print('role name=' + name)
        print('process_user,assign')
        admin_mgr.assign(user, Role(name=name))                
    elif args.operation == DEASSIGN:
        name = args.role        
        print('role name=' + name)        
        print('process_user,deassign')
        admin_mgr.deassign(user, Role(name=name))
    else:
        print('process_user failed, invalid operation=' + args.operation)
        return False
    return True                                
        
def process_role(args):
    role = load_entity (Role(), args)    
    if args.operation == ADD:
        print('process_role,add')
        admin_mgr.add_role(role)        
    elif args.operation == UPDATE:
        print('process_role,update')
        admin_mgr.update_role(role)        
    elif args.operation == DELETE:
        print('process_role,delete')
        admin_mgr.delete_role(role)        
    else:
        print('process_role failed, invalid operation=' + args.operation)
        return False
    return True                                
       
        
def process_object(args):
    object = load_entity (PermObj(), args)    
    if args.operation == ADD:
        print('process_object,add')
        admin_mgr.add_object(object)        
    elif args.operation == UPDATE:
        print('process_object,update')
        admin_mgr.update_object(object)        
    elif args.operation == DELETE:
        print('process_object,delete')
        admin_mgr.delete_object(object)        
    else:
        print('process_object failed, invalid operation=' + args.operation)
        return False
    return True                                
        
        
def process_perm(args):
    perm = load_entity (Perm(), args)        
    if args.operation == ADD:
        print('process_perm,add')
        admin_mgr.add_perm(perm)        
    elif args.operation == UPDATE:
        print('process_perm,update')
        admin_mgr.update_perm(perm)        
    elif args.operation == DELETE:
        print('process_perm,delete')
        admin_mgr.delete_perm(perm)        
    elif args.operation == GRANT:
        name = args.role        
        print('role name=' + name)
        print('process_perm,grant')
        admin_mgr.grant(perm, Role(name=name))                        
    elif args.operation == REVOKE:
        name = args.role        
        print('process_perm,revoke')
        print('role name=' + name)
        admin_mgr.revoke(perm, Role(name=name))                        
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
parser.add_argument('entity', metavar='entity', choices=[USER, ROLE, PERM, OBJECT],
                    help='entity name')
parser.add_argument('operation', metavar='operand', choices=[ADD, UPDATE, DELETE, ASSIGN, DEASSIGN, GRANT, REVOKE],
                    help='operation name')
parser.add_argument('-r', '--role', dest='role',
                    help='role name')

add_args (parser, Role())
add_args (parser, User())
add_args (parser, Perm())    
args = parser.parse_args()
#print(args)
process(args)