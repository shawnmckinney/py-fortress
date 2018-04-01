'''
Created on Mar 28, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''
import argparse
from argparse import ArgumentError

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

AUTH = 'auth'
CHCK = 'check'
ROLES = 'roles'
PERMS = 'perms'
SHOW = 'show'
DROP = 'drop'

def load_entity (entity, args):
    for name in entity.__dict__:
        value = args.__dict__[name]
        if value:
            entity.__dict__[name] = value
            if name != 'password':
                print(name + '=' + str(value))
    return entity

def add_args (parser, entity):
    for name in entity.__dict__:
        try:
            parser.add_argument('--' + name)
        except ArgumentError as e:
            #ignore
            pass

    