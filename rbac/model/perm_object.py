'''
@copyright: 2022 - Symas Corporation
'''
class PermObj:    
    "Fortress Permission Object"
    def __init__(
            self,
            obj_name=None,
            description=None,
            internal_id=None,
            ou=None,
            type=None,
            props=None,
            dn=None
            ):
        self.obj_name=obj_name
        self.description=description
        self.internal_id=internal_id
        self.ou=ou
        self.type=type
        self.props=props
        self.dn=dn