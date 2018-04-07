#!/usr/local/bin/python2.7
# encoding: utf-8
'''
 -- shortdesc

 is a description

It defines classes_and_methods

@author:      smckinn
@copyright:   2018 - Symas Corporation
'''
import sys
import pickle
import argparse
from pyfortress.util import global_ids
from pyfortress.model import Perm, User
from pyfortress.impl import access_mgr
from pyfortress.util import FortressError
from pyfortress.test import print_user, print_entity
from pyfortress.test.cli_utils import (
    load_entity, add_args, ADD, DELETE, AUTH, CHCK, ROLES, PERMS, SHOW, DROP
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
            if not args.role:
                print("error --role required for this op")    
                return False            
            print('role=' + args.role)
            access_mgr.add_active_role(sess, args.role)
            result = True
        elif args.operation == DROP:
            sess = un_pickle()
            if not args.role:
                print("error --role required for this op")    
                return False            
            print('role=' + args.role)            
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
        if e.id == global_ids.ACTV_FAILED_DAY:
            print('failed day of week, id=' + str(e.id) + ', msg=' + e.msg)
        elif e.id == global_ids.ACTV_FAILED_DATE:
            print('failed for date, id=' + str(e.id) + ', msg=' + e.msg)
        elif e.id == global_ids.ACTV_FAILED_TIME:
            print('failed for time of day, id=' + str(e.id) + ', msg=' + e.msg)
        elif e.id == global_ids.ACTV_FAILED_TIMEOUT:
            print('failed inactivity timeout, id=' + str(e.id) + ', msg=' + e.msg)
        elif e.id == global_ids.ACTV_FAILED_LOCK:
            print('failed locked date')
        else:
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


def main(argv=None):
    '''Command line options.'''
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = 'Process py-fortress access_mgr commands.'
    parser = argparse.ArgumentParser(description=program_name)        
    parser.add_argument('operation', metavar='operand', choices=[AUTH,CHCK,ROLES,PERMS,ADD,DELETE,SHOW,DROP], help='operation name')
    parser.add_argument('-r', '--role', dest='role', help='role name')
    add_args(parser, User())
    add_args(parser, Perm())    
    args = parser.parse_args()
    process(args)


if __name__ == "__main__":    
    sys.exit(main())