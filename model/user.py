'''
Created on Feb 10, 2018

@author: smckinney
'''
# Copyright 2018 - Symas Corporation

class User:    
    "Fortess User"

    def __init__(
            self,
            uid=None,
            password=None,
            ou=None,
            internalId=None,
            constraint=None,            
            roleConstraints=None,            
            roles=None,
            pwPolicy=None,
            cn=None,
            sn=None,
            dn=None,
            description=None,
            displayName=None,
            employeeType=None,
            title=None,
            phones=None,
            mobiles=None,
            emails=None,
            reset = None,
            lockedTime = None,
            system = None,
            props = None,
            departmentNumber = None,
            l = None,
            physicalDeliveryOfficeName = None,
            postalCode = None,
            roomNumber = None,                        
            ):
        self.uid = uid
        self.password = password
        self.ou = ou
        self.internalId = internalId
        self.constraint = constraint        
        self.roleConstraints = roleConstraints        
        self.roles = roles
        self.pwPolicy = pwPolicy        
        self.cn = cn       
        self.sn = sn
        self.dn = dn
        self.description = description
        self.displayName = displayName
        self.employeeType = employeeType
        self.title = title
        self.phones = phones
        self.mobiles = mobiles
        self.emails = emails
        self.reset = reset
        self.lockedTime = lockedTime
        self.system = system
        self.props = props        
        self.departmentNumber = departmentNumber
        self.l = l
        self.physicalDeliveryOfficeName = physicalDeliveryOfficeName
        self.postalCode = postalCode
        self.roomNumber = roomNumber