'''
@copyright: 2022 - Symas Corporation
'''

from rbac.model import User, Constraint

ALL = 'all'
NONE = 'none'
BEGIN_DATE = '20180101'
END_DATE = '20501010'
BEGIN_LOCK_DATE = NONE
END_LOCK_DATE = NONE
BEGIN_TIME = '0000'
END_TIME = '0000'
TIMEOUT = 15

def get_test_users(name, total):
    usrs = []
    for i in range(total):
        usrs.append(__create_test_user( name, i))
    return usrs

    
def __create_test_user(name, number):
    
    label = name + '-' + str(number)
    return User(
        uid=label, 
        description=label + ' Role',
        password='password',
        ou='py-test',                    
        sn=label,
        cn=label,                
        display_name=label,
        employee_type='test',
        title='test',
        phones=['111-111-1111', '222-222-2222'],
        mobiles=['333-333-3333', '444-444-4444'],
        emails=['foo@apache.org', 'foo2@apache.org'],
        system = False,
        props = ['name1:value1', 'name2:value2'],
        department_number = '456',
        l = 'Somewhere',
        physical_delivery_office_name = 'Someplace',
        postal_code = '55555',
        room_number = '222',                        
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