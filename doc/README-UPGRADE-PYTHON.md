# py-fortress UPGRADE-PYTHON
-------------------------------------------------------------------------------
## Table of Contents

 * Document Overview
 * SECTION 1. Prerequisites
 * SECTION 2. Setup Python Runtime
___________________________________________________________________________________
## Document Overview

 * Contains instructions to build and test py-fortress
___________________________________________________________________________________
## SECTION 1. Prerequisites

Minimum hardware requirements:
 * 1 Core
 * 1 GB RAM

Minimum software requirements:
 * RHEL/Debian machine
 * Python >=3.6 
________________________________________________________________________________
## SECTION 2. Setup Python Runtime

### RHEL8

```bash
yum install python3-devel openldap-devel 
```

#### Debian

```bash
apt-get install python3-dev python3-venv libldap2-dev ldap-utils libsasl2-dev build-essential
```

#### End of # py-fortress README-UPGRADE-PYTHON