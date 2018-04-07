# py-fortress README

_**Fortress Role-Based Access Control**_ 
![py-fortress](images/FortressLogo-small.png "fortress rbac")

## Document Contents
 * Links to Install and Setup Docs
 * About py-fortress and Role-Based Access Control
________________________________
## Links to Install and Setup Docs
Located under the [doc](pyfortress/doc) folder and include:

|   | Link                                                              | Description                     | 
|---|:------------------------------------------------------------------|:--------------------------------| 
|1. |[README-BUILDING](pyfortress/doc/README-BUILDING.md)               |To build the package from source |
|2. |[README-QUICKSTART](pyfortress/doc/README-QUICKSTART.md)           |Beginners start here             | 
|3. |[README-LDAP-DOCKER](pyfortress/doc/README-LDAP-DOCKER.md)         |Run LDAP in Docker               |
|4. |[README-INSTALL](pyfortress/doc/README-INSTALL.md)                 |Install with PyPI Package        | 
|5. |[README-API](pyfortress/doc/README-API.md)                         |API Usage Guide                  |
|6. |[README-CLI](pyfortress/doc/README-CLI.md)                         |CLI for RBAC Admin and Review    |  
|7. |[README-CLI-AUTH](pyfortress/doc/README-CLI-AUTH.md)               |CLI for RBAC System Testing      | 
_________________________________________________________________________________
## About py-fortress and Role-Based Access Control

### About py-fortress
 * Security access control APIs for the Python3 platform.
 * Requires an *LDAP* server to store the policy data. Support for a *File* backend in the works.
 * Published to PyPI as [py-fortress](https://pypi.org/project/py-fortress/).
 * Compliant with *ANSI INCITS 359* RBAC0, a.k.a "Core RBAC".    
 * Sponsored by [SYMAS](https://symas.com/)
 * Released under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

#### Links to the API Modules
The following modules have inline code docs describing the API signatures, required attributes and usages.

|   | Link                                        | Description                                          |  
|---|:--------------------------------------------|:-----------------------------------------------------|  
|1. |[access_mgr](pyfortress/impl/access_mgr.py)  |create session, check access, add, drop active roles  |  
|2. |[admin_mgr](pyfortress/impl/admin_mgr.py)    |add, update, delete, assign, deassign entities        |  
|3. |[review_mgr](pyfortress/impl/review_mgr.py)  |read and search entities and their relationships      |  
   
#### Related Project
We're related to the [Apache Fortress](http://directory.apache.org/fortress) Java implementation and share:
 * Data Format:
    * [Apache Fortress LDAP schema](https://github.com/apache/directory-fortress-core/blob/master/ldap/schema/fortress.schema)
 * Exception Ids:
    * [org.apache.directory.fortress.core.SecurityException](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/SecurityException.html)
 * Method names and signatures:
    * [Interface AccessMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/AccessMgr.html)
    * [Interface AdminMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/AdminMgr.html)
    * [Interface ReviewMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/ReviewMgr.html)
 * Management interfaces. Entries created by one can be processed by the other, and can be managed using Apache Fortress' Web and Rest interfaces:
    * [Apache Fortress Web](https://github.com/apache/directory-fortress-commander)
    * [Apache Fortress Rest](https://github.com/apache/directory-fortress-enmasse)
     
The Apache Fortress Core has capabilities that py-fortress doesn't, like Hierarchical Roles (RBAC1), Static Separation of Duties (RBAC2) and Dynamic Separation of Duties (RBAC3).   
     
### About Role-Based Access Control
 ![RBAC Core](images/RbacCore.png "RBAC0 - The 'Core'")
 * Many-to-many relationship between Users, Roles and Permissions. Selective Role activation into Sessions. API to
 add, update, delete and search entity data; perform access control decisions during runtime.
 * Link to [ANSI INCITS 359 Specification](http://profsandhu.com/journals/tissec/ANSI+INCITS+359-2004.pdf) 

#### More RBAC info
 * [Intro to RBAC](http://directory.apache.org/fortress/user-guide/1-intro-rbac.html)
 * [The Seven Steps of Role Engineering](https://iamfortress.net/2015/03/05/the-seven-steps-of-role-engineering/)