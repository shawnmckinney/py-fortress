'''
Created on Mar 17, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

from model import PermObj


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