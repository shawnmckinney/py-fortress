'''
Created on Mar 17, 2018

@author: smckinn
@copyright: 2018 - Symas Corporation
'''

class Role:    
    "Fortress Role"
    def __init__(
            self,            
            name=None,
            internal_id=None,
            description=None,
            parents=None,
            children=None,            
            props=None,
            constraint=None,
            dn=None
            ):
        self.name=name
        self.internal_id=internal_id
        self.description=description
        self.parents=parents
        self.children=children
        self.props=props
        self.constraint=constraint
        self.dn=dn