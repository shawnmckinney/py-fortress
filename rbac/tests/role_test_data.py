'''
@copyright: 2022 - Symas Corporation
'''

from rbac.model import Role, Constraint

ALL = 'all'
NONE = 'none'
BEGIN_DATE = '20180101'
END_DATE = '20501010'
BEGIN_LOCK_DATE = NONE
END_LOCK_DATE = NONE
BEGIN_TIME = '0000'
END_TIME = '0000'
TIMEOUT = 15

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
            begin_lock_date=BEGIN_LOCK_DATE,
            end_lock_date=END_LOCK_DATE,
            day_mask=ALL
        )
    )