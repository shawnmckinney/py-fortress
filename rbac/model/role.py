'''
@copyright: 2022 - Symas Corporation
'''

class Role:    
    "Fortress Role"
    def __init__(
            self,            
            name=None,
            internal_id=None,
            description=None,
            props=None,
            constraint=None,
            members=None,
            dn=None
            ):
        self.name=name
        self.internal_id=internal_id
        self.description=description
        self.props=props
        self.constraint=constraint
        self.dn=dn
        self.members=members