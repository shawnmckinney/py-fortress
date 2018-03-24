'''
Created on Mar 23, 2018

@author: smckinn
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
    if args.entity == USER:
        process_user(args)
    elif args.entity == ROLE:
        process_role(args)        
    elif args.entity == PERM:
        process_perm(args)                
    elif args.entity == OBJECT:
        process_object(args)
        
                        
def load_entity (entity, args):
    for name in entity.__dict__:
        value = args.__dict__[name]
        if value:
            entity.__dict__[name] = value
    return entity

    
def process_user(args):
    print('process_user')    
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
        print('process_user,assign')
        name = args.role
        admin_mgr.assign(user, Role(name=name))                
    elif args.operation == DEASSIGN:
        print('process_user,deassign')
        name = args.role
        admin_mgr.deassign(user, Role(name=name))                
        
        
def process_role(args):
    print('process_role')    
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
       
        
def process_object(args):
    print('process_object')
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
        
        
def process_perm(args):
    print('process_perm')
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
        print('process_perm,grant')
        name = args.role
        admin_mgr.grant(perm, Role(name=name))                        
    elif args.operation == REVOKE:
        print('process_perm,revoke')
        name = args.role
        admin_mgr.revoke(perm, Role(name=name))                        
        
        
def add_attrs (parser, entity):
    for name in entity.__dict__:
        try:
            parser.add_argument('--' + name)
        except ArgumentError as e:
            print('ArgumentError=' + str(e))


parser = argparse.ArgumentParser(description='Process py-fortress commands.')
parser.add_argument('entity', metavar='entity', choices=[USER, ROLE, PERM, OBJECT],
                    help='entity name')
parser.add_argument('operation', metavar='operand', choices=[ADD, UPDATE, DELETE, ASSIGN, DEASSIGN, GRANT, REVOKE],
                    help='operation name')
parser.add_argument('-u', '--uid', dest='uid',
                    help='userid')
parser.add_argument('-r', '--role', dest='role',
                    help='role nm')

add_attrs (parser, Role())
add_attrs (parser, User())
add_attrs (parser, Perm())    
args = parser.parse_args()
print(args)
process(args)