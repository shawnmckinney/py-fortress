# py-fortress README

_**Fortress Role-Based Access Control**_ 
![py-fortress](images/FortressLogo-small.png "fortress rbac")

## Document Contents
 * SECTION 1 - Intro to py-fortress and RBAC
 * SECTION 2 - Links to Install and Setup Docs
__________________________________________________________________________________
## SECTION 1. Intro to py-fortress and RBAC

### About py-fortress
 * Compliant with *ANSI INCITS 359* Role-Based Access Control, RBAC0, aka Core RBAC.
 * Data stored in LDAP. Support for other backends in the works.
 * Python APIs and CLI to manage and interrogate the security policy data.
 * Published to [PyPI](https://pypi.python.org/pypi/py-fortress)
 * Released as open source, Apache License v2.0 

#### Links to the Python RBAC modules
These APIs have inline code docs describing the method signatures and required attributes. 
 * [access_mgr](https://github.com/shawnmckinney/py-fortress/blob/master/pyfortress/impl/access_mgr.py): performs runtime access control operations
 * [admin_mgr](https://github.com/shawnmckinney/py-fortress/blob/master/pyfortress/impl/admin_mgr.py): performs administrative functions that provision entities into their backend datastore 
 * [review_mgr](https://github.com/shawnmckinney/py-fortress/blob/master/pyfortress/impl/review_mgr.py): administrative review functions on the RBAC entities.
   
#### Related Project
We're related to the [Apache Fortress](http://directory.apache.org/fortress) Java implementation that we have common...
 * Data Format:
    * [Apache Fortress LDAP schema](https://github.com/apache/directory-fortress-core/blob/master/ldap/schema/fortress.schema)
 * Exception Ids:
    * [org.apache.directory.fortress.core.SecurityException](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/SecurityException.html)
 * Method names and signatures:
    * [Interface AccessMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/AccessMgr.html)
    * [Interface AdminMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/AdminMgr.html)
    * [Interface ReviewMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/ReviewMgr.html)
    
There're many things that the Apache Fortress Core can do that this project can't; Hierarchical Roles (RBAC1), Static Separation of Duties (RBAC2) and Dynamic Separation of Duties (RBAC3) to name a few.
_*So there's work yet to be done here*_.    
     
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
__________________________________________________________________________________
## SECTION 2. Links to Install and Setup Docs
1. If you're new to fortress: [LDAP SERVER QUICKSTART](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-QUICKSTART.md) 
2. Install the py-fortress python package using pip: [py-fortress Installation](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-INSTALL.md)
3. How the APIs work: [API Usage Guide](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-API.md)
4. Use the CLI to setup and test: [Guide to Command Line Interpreter (CLI) for RBAC0 SYSTEM Testing](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-CLI-AUTH.md)  
5. Use the CLI to administer and interrogate: [Guide to Admin and Review CLI](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-CLI.md)  
