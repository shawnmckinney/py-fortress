# py-fortress README

_**Fortress Role-Based Access Control**_ 
![py-fortress](images/FortressLogo-small.png "fortress rbac")

## Document Contents
 * Links to Install and Setup Docs
 * Intro to py-fortress and RBAC
__________________________________________________________________________________
## Links to Install and Setup Docs

|   | Link                                                    | Description                  | 
|---|:--------------------------------------------------------|:-----------------------------| 
|1. |[README-QUICKSTART](pyfortress/doc/README-QUICKSTART.md) |Beginners Guide   | 
|2. |[README-INSTALL](pyfortress/doc/README-INSTALL.md)       |Install Guide                 | 
|3. |[README-API](pyfortress/doc/README-API.md)               |API Usage Guide               | 
|4. |[README-CLI-AUTH](pyfortress/doc/README-CLI-AUTH.md)     |CLI for RBAC System           | 
|5. |[README-CLI](pyfortress/doc/README-CLI.md)               |CLI for RBAC Admin and Review | 
_________________________________________________________________________________
## Intro to py-fortress and RBAC

### About py-fortress
 * Compliant with *ANSI INCITS 359* Role-Based Access Control, RBAC0, aka Core RBAC.
 * Data stored in LDAP. Support for other backends in the works.
 * Python APIs and CLI to manage and interrogate the security policy data.
 * Published to [PyPI](https://pypi.python.org/pypi/py-fortress)
 * Released as open source, Apache License v2.0 

#### Links to the RBAC APIs
These APIs have inline code docs describing the method signatures and required attributes.

|   | Link                                        | Description                                          |  
|---|:--------------------------------------------|:-----------------------------------------------------|  
|1. |[access_mgr](pyfortress/impl/access_mgr.py)  |create session, check access, add, drop active roles  |  
|2. |[admin_mgr](pyfortress/impl/admin_mgr.py)    |add, update, delete, assign, deassign entities        |  
|3. |[review_mgr](pyfortress/impl/review_mgr.py)  |read and search entities and their relationships      |  
   
#### Related Project
We're related to the [Apache Fortress](http://directory.apache.org/fortress) Java implementation sharing...
 * Data Format:
    * [Apache Fortress LDAP schema](https://github.com/apache/directory-fortress-core/blob/master/ldap/schema/fortress.schema)
 * Exception Ids:
    * [org.apache.directory.fortress.core.SecurityException](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/SecurityException.html)
 * Method names and signatures:
    * [Interface AccessMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/AccessMgr.html)
    * [Interface AdminMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/AdminMgr.html)
    * [Interface ReviewMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/ReviewMgr.html)
 * Management interfaces. Data created by one can be used by the other, e.g. can be managed using the apache fortress gui and rest impls:
    * [Apache Fortress Web](https://github.com/apache/directory-fortress-commander)
    * [Apache Fortress Rest](https://github.com/apache/directory-fortress-enmasse)
     
Apache Fortress Core has RBAC capabilities that py-fortress can't do, namely Hierarchical Roles (RBAC1), Static Separation of Duties (RBAC2) and Dynamic Separation of Duties (RBAC3).
_*There's more work to do*_.    
     
### About Role-Based Access Control
 ![RBAC Core](images/RbacCore.png "RBAC0 - The 'Core'")
 * Many-to-many relationship between Users, Roles and Permissions. Selective role activation into sessions. 
API to add, update, delete identity data and perform identity and access control decisions during runtime operations
 * The RBAC functional specification describes operations for the creation and maintenance of RBAC element sets and relations; 
review functions for performing queries; and system functions for creating and managing sessions, and making access control decisions.
 * [Link to ANSI INCITS 359 Specification](http://profsandhu.com/journals/tissec/ANSI+INCITS+359-2004.pdf)

#### More info
 * [Intro to RBAC](http://directory.apache.org/fortress/user-guide/1-intro-rbac.html)
 * [The Seven Steps of Role Engineering](https://iamfortress.net/2015/03/05/the-seven-steps-of-role-engineering/)