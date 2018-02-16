'''
Created on Feb 16, 2018

@author: smckinn
'''
# Copyright 2018 - Symas Corporation

class Permission:    
    "Fortess Permission"
    def __init__(
            self,
            objName=None,
            opName=None,
            objId=None,
            description=None,
            abstractName=None,
            internalId=None,
            type=None,
            users=None,
            roles=None,
            props=None,
            dn=None
            ):
        self.objName=objName
        self.opName=opName
        self.objId=objId
        self.description=description
        self.abstractName=abstractName
        self.internalId=internalId
        self.type=type
        self.users=users
        self.roles=roles
        self.props=props
        self.dn=dn