'''
Created on Mar 17, 2018

@author: smckinn
'''

from model import Role, Constraint

NAME = 'py-fortress-test-'
idx = 1
ALL = 'all'
NONE = 'none'
BEGIN_DATE = '20180101'
END_DATE = '20501010'
BEGIN_LOCK_DATE = ''
END_LOCK_DATE = ''
BEGIN_TIME = '0000'
END_TIME = '0000'
TIMEOUT = 0

def get_test_roles(name, total):
    rles = []
    
    for i in range(total):
        rles.append(__create_test_role( name, i))
    return rles

    
def __create_test_role(name, number):
    
    label = name + '-' + str(number)
    return Role(
        name=label, 
        description=label + ' Role',
        constraint=Constraint(
            name=label,
            timeout=TIMEOUT,
            begin_time=BEGIN_TIME,
            end_time=END_TIME,
            begin_date=BEGIN_DATE,
            end_date=END_DATE,
            begin_lock_date=NONE,
            end_lock_date=NONE,
            day_mask=ALL
        )
    )
    
rles1 = [
    Role(
        name=NAME + '1', 
        description=NAME + ' Role',
        constraint=Constraint(
            name=NAME + '1',
            timeout=TIMEOUT,
            begin_time=BEGIN_TIME,
            end_time=END_TIME,
            begin_date=BEGIN_DATE,
            end_date=END_DATE,
            begin_lock_date=NONE,
            end_lock_date=NONE,
            day_mask=ALL
        )
    ),
]


    