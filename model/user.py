'''
Created on Feb 10, 2018

@author: smckinney
'''

class User:    
    "Fortess User"

    def __init__(
            self,
            uid=None,
            password=None,
            ou=None,
            internalId=None,
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
            
            #constraint=None,
#             x=None,
#             x=None,
#             x=None,
#             x=None,
#             x=None,
#             x=None,
                        
            ):
        self.uid = uid
        self.password = password
        self.ou = ou
        self.internalId = internalId
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
        
        #self.constraint = constraint
        
#         self.x = x
#         self.x = x
#         self.x = x
#         self.x = x
#         self.x = x
#         self.x = x
#     private Address address;
#     private List<UserRole> roles;
#     private List<UserAdminRole> adminRoles;
#     private byte[] jpegPhoto;
# 
        
#             beginTime=None,
#             endTime=None,
#             beginDate=None,
#             endDate=None,
#             beginLockDate=None,
#             endLockDate=None,
#             dayMask=None,
#     private int timeout;

#         self.beginTime = beginTime
#         self.endTime = endTime
#         self.beginDate = beginDate
#         self.endDate = endDate
#         self.beginLockDate = beginLockDate
#         self.endLockDate = endLockDate
#         self.dayMask = dayMask