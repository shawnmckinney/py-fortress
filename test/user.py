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
            ):
        self.uid = uid
        self.password = password
        self.ou = ou
        
#     private String userId;
#     private String password;
#     private String newPassword;
#     private String internalId;
#     private List<UserRole> roles;
#     private List<UserAdminRole> adminRoles;
#     private String pwPolicy;
#     private String cn;
#     private String sn;
#     private String dn;
#     private String ou;
#     private String displayName;
#     private String description;
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
        
