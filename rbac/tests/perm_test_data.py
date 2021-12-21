'''
@copyright: 2012 - Symas Corporation
'''

from rbac.model import PermObj, Perm
from enum import Enum


def get_test_objs(name, total):
    objs = []
    for i in range(total):
        objs.append(__create_test_obj( name, i))
    return objs

    
def __create_test_obj(name, number):    
    label = name + '-' + str(number)
    return PermObj(
        obj_name=label, 
        description=label + ' Object',
        ou='py-test',
        type='test',
        props = ['name1:value1', 'name2:value2']        
    )
    
    
def get_test_perms(name, total):
    perms = []
    for i in range(total):
        for op in Operations:             
            perms.append(__create_test_perm( name, i, op.name))
    return perms

    
def __create_test_perm(name, number, op):    
    label = name + '-' + str(number)
    return Perm(
        obj_name=label,
        op_name=op, 
        obj_id=str(number),
        description=label + ' Object.' + op,
        abstract_name=label + '.' + op,
        type='test',
        props = ['name1:value1', 'name2:value2']        
    )    
    
    
class Operations(Enum):
    ADD = 1
    UPDATE = 2
    DELETE = 3
    READ = 4
    SEARCH = 5
    LOAD = 6
    MONITOR = 7
    NOTIFY = 8
    TERMINATE = 9
    INITIATE = 10
        