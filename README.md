# Role-Based Access Control API for Python

-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Introduction 
 * SECTION 2. Prerequisites
 * SECTION 3. Setup using ApacheDS or OpenLDAP Docker Image
 * SECTION 4. Integration Test
 * SECTION 5. Simple Test Samples 
 * SECTION 6. Docker Commands
___________________________________________________________________________________
## Document Overview

 * This document contains instructions to install py-fortress using either ApacheDS or OpenLDAP Docker image.
___________________________________________________________________________________
## SECTION 1. Introduction

### About py-fortress
 * Compliant with *ANSI INCITS 359* Role-Based Access Control, *RBAC0*, aka *Core RBAC*.
 * Data stored within an LDAPv3 directory server
 * Includes Python APIs to manage and interrogate the security policy data.
 * Compatible with [Apache Fortress LDAP schema](https://github.com/apache/directory-fortress-core/blob/master/ldap/schema/fortress.schema)

### About Role-Based Access Control

[Link to ANSI INCITS 359 Specification](http://profsandhu.com/journals/tissec/ANSI+INCITS+359-2004.pdf)

Many-to-many relationship between Users, Roles and Permissions. Selective role activation into sessions. 
API to add, update, delete identity data and perform identity and access control decisions during runtime operations

 ![RBAC Core](images/RbacCore.png "RBAC0 - The 'Core'")
 
The RBAC functional specification (contained within the above link) describes administrative operations for the creation and maintenance of RBAC element sets and relations; 
administrative review functions for performing administrative queries; and system functions for creating and managing RBAC attributes on 
user sessions and making access control decisions.

### About the APIs
Links to the Python RBAC modules containing inline docs describing their use.
 * [access_mgr](impl/access_mgr.py): performs runtime access control operations
 * [admin_mgr](impl/admin_mgr.py): performs administrative functions that provision entities into their backend datastore 
 * [review_mgr](impl/review_mgr.py): administrative review functions on the RBAC entities. 
  
### More on RBAC
 * [Intro to RBAC](http://directory.apache.org/fortress/user-guide/1-intro-rbac.html)
 * [The Seven Steps of Role Engineering](https://iamfortress.net/2015/03/05/the-seven-steps-of-role-engineering/)

### Related Projects
 * [Apache Fortress](http://directory.apache.org/fortress)
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
    export CONTAINER_ID=$(docker run -d -P apachedirectory/apacheds-for-apache-fortress-tests)
    export CONTAINER_PORT=$(docker inspect --format='{{(index (index .NetworkSettings.Ports "10389/tcp") 0).HostPort}}' $CONTAINER_ID)
    echo $CONTAINER_PORT
    ```
       
    b. slapd 
    ```
    export CONTAINER_ID=$(docker run -d -P apachedirectory/openldap-for-apache-fortress-tests)
    export CONTAINER_PORT=$(docker inspect --format='{{(index (index .NetworkSettings.Ports "389/tcp") 0).HostPort}}' $CONTAINER_ID)
    echo $CONTAINER_PORT
    ```

    * make note of the port, it's needed later
    * depending on your docker setup may need to run as root or sudo priv's.
__________________________________________________________________________________
## SECTION 4. Integration Tests

1. Prepare py-fortress to use the directory server running inside docker container:

    This uses the `$CONTAINER_PORT` from above to edit the port automatically:

    ```
    python3 test/edit-config.py
    ```

2. Update the connection parameters, if needed:

    ```
    vi test/py-fortress-cfg.json
    ```

    a. apacheds:
    ```
    "dn": "uid=admin,ou=system",
    ```
    
    b. slapd:
    ```
    "dn": "cn=Manager,dc=example,dc=com",
    ```

3. Save and exit

4. Prepare your terminal for execution of python3.  From the main dir of the git repo:

    ```
    pyvenv env
    . env/bin/activate
    pip3 install ldap3
    export PYTHONPATH=$(pwd)
    cd test
    ```

5. This program prepare the Directory Information Tree (DIT) by creating four nodes for policy storage:
    * Suffix (dc=example,dc=com)
    * People (ou=People,dc=example,dc=com)
    * Roles (ou=Roles,dc=example,dc=com)
    * Permissions (ou=Perms,dc=example,dc=com)
    ```
    python3 test_dit_dao.py 
    ```
    
    *The suffix and container distinguished names (dn) parameters are required here:* **[py-fortress-cfg](test/py-fortress-cfg.json)** 
    
6. Run the admin mgr tests:
    ```
    python3 test_admin_mgr.py 
    ```

7. Run the access mgr tests:
    ```
    python3 test_access_mgr.py 
    ```
 
8. Run the review mgr tests:
    ```
    python3 test_review_mgr.py 
    ```
__________________________________________________________________________________
## SECTION 5. Simple Test Samples

The [test_samples](test/test_samples.py) module has simple tests.  
 
1. Run the samples:
    ```
    python3 test_samples.py 
    ```

2. View the samples to learn how the APIs work.
____________________________________________________________________________________
## SECTION 6. Docker Commands

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
