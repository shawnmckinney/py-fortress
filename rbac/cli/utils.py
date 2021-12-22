'''
@copyright: 2022 - Symas Corporation
'''
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


def print_ln(ln, num=None):
    if num is None:
        num = 0
    tabs = ''
    for x in range(0, num):
        tabs += '\t'
    print(tabs + ln)
    #logger.debug((tabs + ln))


def print_entity(entity, label, indent=None):
    if indent is None:
        indent = 1
    print_ln(label, indent - 1)
    for name in entity.__dict__:
        if name != 'password':
            value = entity.__dict__[name]
            if value:
                print_ln("\t{0}: {1}".format(name, value), indent)


def print_user(entity, label):
    print_entity(entity, label, 1)
    if entity.constraint is not None:
        print_entity(entity.constraint, "User Constraint:", 2)

    if entity.role_constraints is not None:
        for idx, constraint in enumerate(entity.role_constraints):
            # print_constraint (constraint, "User-Role Constraint[" + str(idx+1) + "]:")
            if constraint.name:
                print_entity(constraint, "User-Role Constraint[" + str(idx + 1) + "]:", 2)
    print_ln("*************** " + label + " *******************")


def print_role(entity, label):
    print_entity(entity, label, 1)
    if entity.constraint is not None and entity.constraint.name:
        print_entity(entity.constraint, "Role Constraint:", 2)
    print_ln("*************** " + label + " *******************")
