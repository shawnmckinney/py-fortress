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
 * Data stored within an LDAPv3 directory server
 * Includes Python APIs to manage and interrogate the security policy data.
 * Compatible with [Apache Fortress LDAP schema](https://github.com/apache/directory-fortress-core/blob/master/ldap/schema/fortress.schema)

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
  
### More on RBAC
 * [Intro to RBAC](http://directory.apache.org/fortress/user-guide/1-intro-rbac.html)
 * [The Seven Steps of Role Engineering](https://iamfortress.net/2015/03/05/the-seven-steps-of-role-engineering/)

### Related Projects
py-fortress is compatible with Apache Fortress by using the exact same data format.
 * [Apache Fortress](http://directory.apache.org/fortress)
__________________________________________________________________________________
## SECTION 2. Installation, Setup and Usage
1. [py-fortress Installation](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-INSTALL.md) 
2. [LDAP Setup](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-QUICKSTART.md) 
3. [Admin and Review Manager Command Line Interface](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-CLI.md) 
4. [Access Manager Command Line Interface](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-CLI-AUTH.md) 
5. [API Usage Guide](https://github.com/shawnmckinney/py-fortress/tree/master/pyfortress/doc/README-API.md) 