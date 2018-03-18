# py-fortress
*Work-in-progress*  
 ![Under Construction](images/under-construction.png "py-fortress under construction")
...

# py-fortress setup and test instructions

-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Prerequisites
 * SECTION 2. py-fortress Setup using ApacheDS or OpenLDAP Docker Image
 * SECTION 3. py-fortress Integration Test
 * SECTION 4. Docker Commands
___________________________________________________________________________________
## Document Overview

 * This document contains instructions to install py-fortress using either ApacheDS or OpenLDAP Docker image.
___________________________________________________________________________________
## SECTION 1. Prerequisites

Minimum hardware requirements:
 * 2 Cores
 * 4GB RAM

Minimum software requirements:
 * Centos or Debian Machine
 * docker-engine
 * python3

___________________________________________________________________________________
## SECTION 2. py-fortress Setup using ApacheDS or OpenLDAP Docker Image

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

 *note: make note of the port as it's needed later
 *depending on your docker setup may need to run as root or sudo priv's.

3. Prepare directory server to use py-fortress by initializing the directory information tree:

 a. apacheds
 ```
 ldapmodify -h localhost -p 32770 -D uid=admin,ou=system -w secret -a -f test/py-fortress-dit.ldif 
 ```

 b. slapd
 ```
 ldapmodify -h localhost -p 32770 -D cn=Manager,dc=example,dc=com -w secret -a -f test/py-fortress-dit.ldif 
 ```
 
 *note: use the port *-p* from earlier step

4. Prepare py-fortress to use the directory server running inside docker container:

 ```
 vi test/py-fortress-cfg.json
 ```

5. Update the connection parameters:

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
  
 *note: use the port from earlier step
 
6. Save and exit

7. Prepare your terminal for execution of python3.

8. Run the admin mgr tests:

 ```
 python3 test/test_admin_mgr.py 
 ```

9. Run the access mgr tests:

 ```
 python3 test/test_access_mgr.py 
 ```
 
10. Run the review mgr tests:

 ```
 python3 test/test_review_mgr.py 
 ```
 
 ___________________________________________________________________________________
## SECTION 4. Docker Commands

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

____________________________________________________________________________________
#### END OF README