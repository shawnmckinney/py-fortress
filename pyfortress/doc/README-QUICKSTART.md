# py-fortress LDAP Installation Quickstart
-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Prerequisites
 * SECTION 2. Start using ApacheDS or OpenLDAP Docker Image
 * SECTION 3. Setup Python Runtime and Configure py-fortress Usage
 * SECTION 4. Integration Test
 * SECTION 5. Simple Test Samples 
 * SECTION 6. Docker Commands
___________________________________________________________________________________
## Document Overview

 * Contains instructions to install and test py-fortress using an ApacheDS or OpenLDAP Docker image.
 * Many ways of setting up an LDAP server.  Using a docker image is probably the most expedient.
 * For more robust choices, start here: [Options for using Apache Fortress and LDAP](https://github.com/apache/directory-fortress-core/blob/master/README.md).
___________________________________________________________________________________
## SECTION 1. Prerequisites

Minimum hardware requirements:
 * 1 Core
 * 1 GB RAM

Minimum software requirements:
 * Linux machine
 * git
 * docker engine
 * Python3 and virtualenv (venv) or system install of the ldap3 python module
________________________________________________________________________________
## SECTION 2. Start using ApacheDS or OpenLDAP Docker Image

1. Pull the docker image (pick one):

    a. apacheds
    ```
    docker pull apachedirectory/apacheds-for-apache-fortress-tests
    ```

    b. openldap
    ```
    docker pull apachedirectory/openldap-for-apache-fortress-tests
    ```

2. Run the docker container (pick one):

    a. apacheds
    ```
    export CONTAINER_ID=$(docker run -d -P apachedirectory/apacheds-for-apache-fortress-tests)
    export CONTAINER_PORT=$(docker inspect --format='{{(index (index .NetworkSettings.Ports "10389/tcp") 0).HostPort}}' $CONTAINER_ID)
    echo $CONTAINER_PORT
    ```
       
    b. openldap 
    ```
    export CONTAINER_ID=$(docker run -d -P apachedirectory/openldap-for-apache-fortress-tests)
    export CONTAINER_PORT=$(docker inspect --format='{{(index (index .NetworkSettings.Ports "389/tcp") 0).HostPort}}' $CONTAINER_ID)
    echo $CONTAINER_PORT
    ```

    * make note of the port, it's needed later
    * depending on your docker setup may need to run as root or sudo priv's.
________________________________________________________________________________
## SECTION 3. Setup Python Runtime and Configure py-fortress Usage

1. Clone py-fortress
    ```
    git clone https://github.com/shawnmckinney/py-fortress.git
    ```

2. Change directory into root folder of project:
    ```
    cd py-fortress
    ```

3. Now edit config file:
    ```
    vi pyfortress/test/py-fortress-cfg.json
    ```

4. Set the LDAP Port
    ```
    ...
    "ldap": {
      ...
      "port": 32768,
    ...
    ```
    *use value obtained earler*
        
5. Update the connection parameters (pick one):

    a. apacheds:
    ```
    "dn": "uid=admin,ou=system",
    ```
    
    b. openldap:
    ```
    "dn": "cn=Manager,dc=example,dc=com",
    ```

6. Set the structure in DIT:
    ```
    ...
    "dit": {
        "suffix": "dc=example,dc=com",
        "users": "People",
        "roles": "Roles",
        "perms": "Perms"
    },
    ...    
    ```
    *if in doubt use the defaults*
    
7. Save and exit

8. Prepare your terminal for execution of python3.  From the main dir of the git repo:
    ```
    pyvenv env
    . env/bin/activate
    pip3 install ldap3
    export PYTHONPATH=$(pwd)
    cd pyfortress/test
    ```
    
9. Run the bootstrap pgm that creates the LDAP node structure, i.e. the *DIT*
    ```
    python3 test_dit_dao.py 
    ```
    
    *Locations for these nodes are set in the config file.* 
    
__________________________________________________________________________________
## SECTION 4. Integration Tests

These steps are optional and verify the env is working correctly.

1. Run the admin mgr tests:
    ```
    python3 test_admin_mgr.py 
    ```

2. Run the access mgr tests:
    ```
    python3 test_access_mgr.py 
    ```
 
3. Run the review mgr tests:
    ```
    python3 test_review_mgr.py 
    ```
__________________________________________________________________________________
## SECTION 5. Simple Test Samples

Another optional test.  
 
1. Run the samples:
    ```
    python3 test_samples.py 
    ```

2. View the [test_samples](../test/test_samples.py) and learn how RBAC APIs work.
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
 
 b. openldap
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
