# Role-Based Access Control API for Python

-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Introduction to RBAC and py-fortress 
 * SECTION 2. Prerequisites
 * SECTION 3. Setup using ApacheDS or OpenLDAP Docker Image
 * SECTION 4. Integration Test
 * SECTION 5. Docker Commands
___________________________________________________________________________________
## Document Overview

 * This document contains instructions to install py-fortress using either ApacheDS or OpenLDAP Docker image.
___________________________________________________________________________________
## SECTION 1. Introduction to RBAC and py-fortress

 ![RBAC Core](images/RbacCore.png "RBAC0 - The 'Core'")
 
### About py-fortress
This *Python3* library is compliant with *ANSI INCITS 359* Role-Based Access Control, *RBAC0*, aka *Core RBAC*.
Many-to-many relationship between Users, Roles and Permissions. Selective role activation into sessions. 
API to add, update, delete identity data and perform identity and access control decisions during runtime operations

[Link to ANSI INCITS 359 Specification](http://profsandhu.com/journals/tissec/ANSI+INCITS+359-2004.pdf)

### About RBAC
The RBAC functional specification (contained within the above link) describes administrative operations for the creation and maintenance of RBAC element sets and relations; 
administrative review functions for performing administrative queries; and system functions for creating and managing RBAC attributes on 
user sessions and making access control decisions.

### About the py-fortress RBAC APIs
Click on the links that follow to browse the python modules with RBAC apis, view the code and inline doc describing how they work.*
 * [access_mgr](impl/access_mgr.py): This performs runtime access control operations on objects that are provisioned RBAC entities that reside in LDAP directory.
 * [admin_mgr](impl/admin_mgr.py): This performs administrative functions to provision Fortress RBAC entities into the LDAP directory. 
 * [review_mgr](impl/review_mgr.py): The administrative review functions on already provisioned Fortress RBAC entities that reside in LDAP directory. 
  
### More on RBAC
 * [Intro to RBAC](http://directory.apache.org/fortress/user-guide/1-intro-rbac.html)
 * [The Seven Steps of Role Engineering](https://iamfortress.net/2015/03/05/the-seven-steps-of-role-engineering/)    
___________________________________________________________________________________
## SECTION 2. Prerequisites

Minimum hardware requirements:
 * 2 Cores
 * 4GB RAM

Minimum software requirements:
 * Linux machine
 * docker-engine installed
 * Python3 installed
___________________________________________________________________________________
## SECTION 3. Setup using ApacheDS or OpenLDAP Docker Image

1. Pull the docker image:

    a. apacheds
    ```
    docker pull apachedirectory/apacheds-for-apache-fortress-tests
    ```

    b. slapd
    ```
    docker pull apachedirectory/openldap-for-apache-fortress-tests
    ```

2. Run the docker container:

    a. apacheds
    ```
    CONTAINER_ID=$(docker run -d -P apachedirectory/apacheds-for-apache-fortress-tests)
    CONTAINER_PORT=$(docker inspect --format='{{(index (index .NetworkSettings.Ports "10389/tcp") 0).HostPort}}' $CONTAINER_ID)
    echo $CONTAINER_PORT
    ```
       
    b. slapd 
    ```
    CONTAINER_ID=$(docker run -d -P apachedirectory/openldap-for-apache-fortress-tests)
    CONTAINER_PORT=$(docker inspect --format='{{(index (index .NetworkSettings.Ports "389/tcp") 0).HostPort}}' $CONTAINER_ID)
    echo $CONTAINER_PORT
    ```

    * make note of the port, it's needed later
    * depending on your docker setup may need to run as root or sudo priv's.

3. Prepare directory server to use py-fortress by initializing the directory information tree:

    a. apacheds
    ```
    ldapmodify -h localhost -p 32770 -D uid=admin,ou=system -w secret -a -f test/py-fortress-dit.ldif 
    ```

    b. slapd
    ```
    ldapmodify -h localhost -p 32770 -D cn=Manager,dc=example,dc=com -w secret -a -f test/py-fortress-dit.ldif 
    ```
 
    * use the port *-p* from earlier
__________________________________________________________________________________
## SECTION 4. Integration Tests

1. Prepare py-fortress to use the directory server running inside docker container:

    ```
    vi test/py-fortress-cfg.json
    ```

2. Update the connection parameters:

    a. apacheds:
    ```
    "port": 32770,
    "dn": "uid=admin,ou=system",
    "password": "secret"                
    ```
 
    b. slapd:
    ```
    "port": 32770,
    "dn": "cn=Manager,dc=example,dc=com",
    "password": "secret"                
    ```
  
    * Use the port from earlier
 
3. Save and exit

4. Prepare your terminal for execution of python3.

5. Run the admin mgr tests:

    ```
    python3 test/test_admin_mgr.py 
    ```

6. Run the access mgr tests:

    ```
    python3 test/test_access_mgr.py 
    ```
 
7. Run the review mgr tests:

    ```
    python3 test/test_review_mgr.py 
    ```
____________________________________________________________________________________
## SECTION 5. Docker Commands

Here are some common commands needed to manage the Docker image.

#### Build image

 ```
 docker build -t apachedirectory/apacheds-for-apache-fortress-tests -f src/docker/apacheds-for-apache-fortress-tests/Dockerfile .
 ```

 * trailing dot matters

 Or just to be sure don't use cached layers:

 ```
 docker build   --no-cache=true -t apachedirectory/apacheds-for-apache-fortress-tests -f src/docker/apacheds-for-apache-fortress-tests/Dockerfile .
 ```

#### Run container

 a. apacheds
 ```
 CONTAINER_ID=$(docker run -d -P apachedirectory/apacheds-for-apache-fortress-tests)
 CONTAINER_PORT=$(docker inspect --format='{{(index (index .NetworkSettings.Ports "10389/tcp") 0).HostPort}}' $CONTAINER_ID)
 echo $CONTAINER_PORT
 ```
 
 b. slapd
 ```
 CONTAINER_ID=$(docker run -d -P apachedirectory/openldap-for-apache-fortress-tests)
 CONTAINER_PORT=$(docker inspect --format='{{(index (index .NetworkSettings.Ports "389/tcp") 0).HostPort}}' $CONTAINER_ID)
 echo $CONTAINER_PORT
 ```

#### Go into the container

 ```
 docker exec -it $CONTAINER_ID bash
 ```

#### Restart container

 ```
 docker restart $CONTAINER_ID
 ```

#### Stop and delete container

 ```
 docker stop $CONTAINER_ID
 docker rm $CONTAINER_ID
 ```
_________________________________________________________________________________
#### END OF README