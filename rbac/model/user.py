'''
@copyright: 2022 - Symas Corporation
'''

class User:    
    "Fortress User"

    def __init__(
            self,
            uid=None,
            password=None,
            ou=None,
            internal_id=None,
            constraint=None,            
            role_constraints=None,            
            roles=None,
            pw_policy=None,
            cn=None,
            sn=None,
            dn=None,
            description=None,
            display_name=None,
            employee_type=None,
            title=None,
            phones=None,
            mobiles=None,
            emails=None,
            reset = None,
            locked_time = None,
            system = None,
            props = None,
            department_number = None,
            l = None,
            physical_delivery_office_name = None,
            postal_code = None,
            room_number = None,                        
            ):
        self.uid = uid
        self.password = password
        self.ou = ou
        self.internal_id = internal_id
        self.constraint = constraint        
        self.role_constraints = role_constraints        
        self.roles = roles
        self.pw_policy = pw_policy        
        self.cn = cn       
        self.sn = sn
        self.dn = dn
        self.description = description
        self.display_name = display_name
        self.employee_type = employee_type
        self.title = title
        self.phones = phones
        self.mobiles = mobiles
        self.emails = emails
        self.reset = reset
        self.locked_time = locked_time
        self.system = system
        self.props = props        
        self.department_number = department_number
        self.l = l
        self.physical_delivery_office_name = physical_delivery_office_name
        self.postal_code = postal_code
        self.room_number = room_number