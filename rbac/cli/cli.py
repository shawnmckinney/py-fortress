'''
@copyright: 2022 - Symas Corporation
'''
import sys
import argparse
from rbac.model import PermObj, Perm, User, Role, Constraint
from rbac import review, admin
from rbac.cli.utils import print_user, print_role, print_ln, print_entity
from rbac.util.fortress_error import RbacError
from rbac.cli.utils import (
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
    except RbacError as e:
        print('RbacError id=' + str(e.id) +', ' + e.msg)                        
                        

def process_user(args):
    user = load_entity(User(), args)        
    print(args.entity + ' ' + args.operation)    
    if not args.uid:
        print("error --uid required for entity user")    
        return False
    elif args.operation == ADD:
        if not args.name:
            args.name = args.uid
        constraint = load_entity(Constraint(), args)
        user.constraint = constraint
        admin.add_user(user)
    elif args.operation == UPDATE:
        if args.name is not None:        
            constraint = load_entity(Constraint(), args)
            user.constraint = constraint
        admin.update_user(user)
    elif args.operation == DELETE:
        admin.delete_user(user)
    elif args.operation == ASSIGN:
        role_nm = args.role        
        print('role=' + role_nm)
        admin.assign(user, Role(name=role_nm))
    elif args.operation == DEASSIGN:
        role_nm = args.role        
        print('role name=' + role_nm)        
        admin.deassign(user, Role(name=role_nm))
    elif args.operation == READ:
        print_user(review.read_user(user), user.uid)
        pass
    elif args.operation == SEARCH:
        user.uid += '*'
        users = review.find_users(user)
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
    if not args.name:
        print("error --name required for entity role")    
        return False
    elif args.operation == ADD:
        constraint = load_entity(Constraint(), args)
        role.constraint = constraint
        admin.add_role(role)
    elif args.operation == UPDATE:
        constraint = load_entity(Constraint(), args)
        role.constraint = constraint
        admin.update_role(role)
    elif args.operation == DELETE:
        admin.delete_role(role)
    elif args.operation == READ:
        print_role(review.read_role(role), role.name)
        pass
    elif args.operation == SEARCH:
        role.name += '*'
        roles = review.find_roles(role)
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
    pobject = load_entity (PermObj(), args) 
    print(args.entity + ' ' + args.operation)   
    if not args.obj_name:
        print("error --obj_name required for entity object")    
        return False
    elif args.operation == ADD:
        admin.add_object(pobject)
    elif args.operation == UPDATE:
        admin.update_object(pobject)
    elif args.operation == DELETE:
        admin.delete_object(pobject)
    elif args.operation == READ:
        print_entity(review.read_object(pobject), pobject.obj_name)
        pass
    elif args.operation == SEARCH:
        pobject.obj_name += '*'
        objs = review.find_objects(pobject)
        if len(objs) > 0:
            for idx, obj in enumerate(objs):
                print_entity(obj, pobject.obj_name + ':' + str(idx))
        else:
            print_ln('No matching records found matching filter: ' + pobject.obj_name) 
    else:
        print('process_object failed, invalid operation=' + args.operation)
        return False
    return True                                
        
        
def process_perm(args):
    perm = load_entity (Perm(), args) 
    print(args.entity + ' ' + args.operation)       
    if args.operation == ADD:
        admin.add_perm(perm)
    elif args.operation == UPDATE:
        admin.update_perm(perm)
    elif args.operation == DELETE:
        admin.delete_perm(perm)
    elif args.operation == GRANT:
        role_nm = args.role        
        print('role=' + role_nm)
        admin.grant(perm, Role(name=role_nm))
    elif args.operation == REVOKE:
        role_nm = args.role        
        print('role=' + role_nm)
        admin.revoke(perm, Role(name=role_nm))
    elif args.operation == READ:
        print_entity(review.read_perm(perm), perm.obj_name + '.' + perm.op_name)
        pass
    elif args.operation == SEARCH:
        role_nm = args.role
        userid = args.uid
        prms = []
        label = ''
        if userid:
            label = userid
            prms = review.user_perms(User(uid=userid))
        elif role_nm:
            label = role_nm
            prms = review.role_perms(Role(name=role_nm))
        else:        
            if perm.obj_name:            
                perm.obj_name += '*'
            else:
                perm.obj_name = '*'            
            if perm.op_name:
                perm.op_name += '*'
            else:
                perm.op_name = '*'
            label = perm.obj_name + '.' + perm.op_name            
            prms = review.find_perms(perm)
        if len(prms) > 0:
            for idx, prm in enumerate(prms):
                print_entity(prm, label + ':' + str(idx))
        else:
            print_ln('No matching records found matching filter: ' + label)                                 
    else:
        print('process_perm failed, invalid operation=' + args.operation)
        return False
    return True                                
        
        
def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    parser = argparse.ArgumentParser(description='Process py-fortress admin and review commands.')
    parser.add_argument('entity', metavar='entity', choices=[USER, ROLE, PERM, OBJECT], help='entity name')
    parser.add_argument('operation', metavar='operand', choices=[ADD, UPDATE, DELETE, ASSIGN, DEASSIGN, GRANT, REVOKE, READ, SEARCH], help='operation name')
    parser.add_argument('-r', '--role', dest='role', help='role name')
    parser.add_argument('--phones', nargs="*", default=[])
    parser.add_argument('--mobiles', nargs="*", default=[])
    parser.add_argument('--emails', nargs="*", default=[])
    parser.add_argument('--props', nargs="*", default=[])
        
    add_args(parser, Role())
    add_args(parser, User())
    add_args(parser, Perm())    
    add_args(parser, PermObj())
    add_args(parser, Constraint())
    args = parser.parse_args()
    process(args)

if __name__ == "__main__":    
    sys.exit(main())