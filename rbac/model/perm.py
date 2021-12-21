'''
@copyright: 2022 - Symas Corporation
'''

class Perm:    
    "Fortress Perm"
    def __init__(
            self,
            obj_name=None,
            op_name=None,
            obj_id=None,
            description=None,
            abstract_name=None,
            internal_id=None,
            type=None,
            users=None,
            roles=None,
            props=None,
            dn=None
            ):
        self.obj_name=obj_name
        self.op_name=op_name
        self.obj_id=obj_id
        self.description=description
        self.abstract_name=abstract_name
        self.internal_id=internal_id
        self.type=type
        self.users=users
        self.roles=roles
        self.props=props
        self.dn=dn