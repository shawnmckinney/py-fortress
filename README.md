# Role-Based Access Control API for Python
-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Introduction
 * SECTION 2. Installation, Setup and Usage 
___________________________________________________________________________________
## Document Overview

 * Overview of py-fortress, RBAC and the APIs
 * Pointers to install/setup doc
__________________________________________________________________________________
## SECTION 1. Introduction

### About py-fortress
 * Compliant with *ANSI INCITS 359* Role-Based Access Control, RBAC0, aka Core RBAC.
 * Currently stores data on LDAP server.  Support for other backends like file in the works.
 * Includes Python APIs to manage and interrogate the security policy data.
 * Includes a Command Line Interpreter to manage the data.
 * Published to [PyPI](https://pypi.python.org/pypi/py-fortress)
 * Released open source Apache License v2.0 

### About Role-Based Access Control

[Link to ANSI INCITS 359 Specification](http://profsandhu.com/journals/tissec/ANSI+INCITS+359-2004.pdf)

Many-to-many relationship between Users, Roles and Permissions. Selective role activation into sessions. 
API to add, update, delete identity data and perform identity and access control decisions during runtime operations

 ![RBAC Core](https://github.com/shawnmckinney/py-fortress/blob/master/images/RbacCore.png "RBAC0 - The 'Core'")
 
The RBAC functional specification describes operations for the creation and maintenance of RBAC element sets and relations; 
review functions for performing queries; and system functions for creating and managing sessions, and making access control decisions.

### About the APIs
Links to the Python RBAC modules:
 * [access_mgr](https://github.com/shawnmckinney/py-fortress/blob/master/pyfortress/impl/access_mgr.py): performs runtime access control operations
 * [admin_mgr](https://github.com/shawnmckinney/py-fortress/blob/master/pyfortress/impl/admin_mgr.py): performs administrative functions that provision entities into their backend datastore 
 * [review_mgr](https://github.com/shawnmckinney/py-fortress/blob/master/pyfortress/impl/review_mgr.py): administrative review functions on the RBAC entities.
 
 *The API docs are contained within the above links.* 
  
### If You're New to RBAC
 * [Intro to RBAC](http://directory.apache.org/fortress/user-guide/1-intro-rbac.html)
 * [The Seven Steps of Role Engineering](https://iamfortress.net/2015/03/05/the-seven-steps-of-role-engineering/)

### Related Project
py-fortress is related to [Apache Fortress](http://directory.apache.org/fortress)
 * Compatible data schema: [Apache Fortress LDAP schema](https://github.com/apache/directory-fortress-core/blob/master/ldap/schema/fortress.schema)
 * Compatible error handling: [org.apache.directory.fortress.core.SecurityException](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/SecurityException.html)
 * Similar API format for these interfaces:
     1- [Interface AccessMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/AccessMgr.html)
     2- [Interface AdminMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/AdminMgr.html)
     3- [Interface ReviewMgr](http://directory.apache.org/fortress/gen-docs/latest/apidocs/org/apache/directory/fortress/core/ReviewMgr.html)
__________________________________________________________________________________
## SECTION 2. Installation, Setup and Usage
1. If you're new to fortress: [LDAP SERVER QUICKSTART](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-QUICKSTART.md) 
2. Install the py-fortress python package using pip: [py-fortress Installation](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-INSTALL.md)
3. How the APIs work: [API Usage Guide](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-API.md)
4. Use the CLI to setup and test: [Guide to Command Line Interpreter (CLI) for RBAC0 SYSTEM Testing](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-CLI-AUTH.md)  
5. Use the CLI to administer and interrogate: [Guide to Admin and Review CLI](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-CLI.md)  