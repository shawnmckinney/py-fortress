#!/usr/local/bin/python2.7
# encoding: utf-8
'''
 -- shortdesc

 is a description

It defines classes_and_methods

@author:      smckinn
@copyright:   2018 - Symas Corporation
'''

import pickle
import argparse
from model import Perm, User
from impl import access_mgr
from util.fortress_error import FortressError
from test.utils import print_user, print_entity
from test.cli_utils import (
    load_entity, add_args, ADD, DELETE, AUTH, CHCK, ROLES, PERMS, SHOW
    )

OUT_SESS_FILE = "sess.pickle"

def process(args):
    sess = None
    result = False
    user = load_entity (User(), args)
    perm = load_entity (Perm(), args)
    print(args.operation)        
    try:
        if args.operation == AUTH:
            sess = access_mgr.create_session(user, False)
            result = True
        elif args.operation == CHCK:
            sess = un_pickle()
            result = access_mgr.check_access(sess, perm)
        elif args.operation == ROLES:   
            sess = un_pickle()         
            roles = access_mgr.session_roles(sess)
            for idx, role in enumerate(roles):
                print_entity(role, role.name + ':' + str(idx))
            result = True
        elif args.operation == PERMS:   
            sess = un_pickle()         
            perms = access_mgr.session_perms(sess)
            for idx, perm in enumerate(perms):
                print_entity(perm, perm.obj_name + '.' + perm.op_name + ':' + str(idx))
            result = True
        elif args.operation == SHOW:     
            sess = un_pickle()       
            print_entity(sess, 'session')
            print_user(sess.user, 'user')           
            result = True
        elif args.operation == ADD:
            sess = un_pickle()
            access_mgr.add_active_role(sess, args.role)
            result = True
        elif args.operation == DELETE:
            sess = un_pickle()
            access_mgr.drop_active_role(sess, args.role)
            result = True
        else:
            print('process failed, invalid operation=' + args.operation)        
        if result:
            print('success')
        else: 
            print('failed')
        pickle_it(sess)
            
    except FortressError as e:
        print('FortressError id=' + str(e.id) +', ' + e.msg)
                        
def pickle_it(sess):
    if sess is not None:
        pickling_on = open(OUT_SESS_FILE,"wb")
        pickle.dump(sess, pickling_on)
        pickling_on.close()

def un_pickle():
    pickle_off = open(OUT_SESS_FILE,"rb")
    sess = pickle.load(pickle_off)
    return sess    
    
program_name = 'Process py-fortress access_mgr commands.'
parser = argparse.ArgumentParser(description=program_name)        
parser.add_argument('operation', metavar='operand', choices=[AUTH,CHCK,ROLES,PERMS,ADD,DELETE,SHOW], help='operation name')
parser.add_argument('-r', '--role', dest='role', help='role name')
add_args(parser, User())
add_args(parser, Perm())    
args = parser.parse_args()
process(args)