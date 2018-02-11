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
        
#         self.x = x
#         self.x = x
#         self.x = x
#         self.x = x
#         self.x = x
#         self.x = x

#     private String description;        
#     private String cn;
#     private String sn;
#     private String dn;
#     private String displayName;
#     private String beginTime;
#     private String endTime;
#     private String beginDate;
#     private String endDate;
#     private String beginLockDate;
#     private String endLockDate;
#     private String dayMask;
#     private String name;
#     private String employeeType;
#     private String title;
#     private int timeout;
#     private boolean reset;
#     private boolean locked;
#     private Boolean system;
#     private Props props = new Props();
#     private Address address;
#     private List<String> phones;
#     private List<String> mobiles;
#     private List<String> emails;

#     private List<UserRole> roles;
#     private List<UserAdminRole> adminRoles;
#     @XmlTransient
#     private byte[] jpegPhoto;
# 
#     // RFC2307bis:
#     /*
#     MUST ( cn $ uid $ uidNumber $ gidNumber $ homeDirectory )
#     MAY ( userPassword $ loginShell $ gecos $ description ) )
#      */
#     private String uidNumber;
#     private String gidNumber;
#     private String homeDirectory;
#     private String loginShell;
#     private String gecos;
        
