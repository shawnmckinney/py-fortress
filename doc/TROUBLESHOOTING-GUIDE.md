# py-fortress TROUBLESHOOTING GUIDE
-------------------------------------------------------------------------------

## Document Overview

Common errors encountered during usage.
___________________________________________________________________________________
## Debug options:

To get debug level output of LDAP operations set debug flag in py-fortress-cfg.json:

```python
  "ldap": {
    ...
    "debug": true,
  },
ldap.set_option(ldap.OPT_DEBUG_LEVEL, 255)
```

## 1. Config file not found

```
FAILED (failures=1)
(env) [root@72-14-182-7 py-fortress]# python3 rbac/tests/test_admin.py
Could not locate py-fortress-cfg.json. Was it added to current directory or user home directory or /etc/pyfortress or env var: PYFORTRESS_CONF
```

Remedy: Ensure py-fortress-cfg.json is available per [README-TESTING](./README-TESTING.md)

```
# TLS_CACERT  fully qualified path and filename of CA certificate file
# For example:
TLS_CACERT  /opt/symas/etc/openldap/certs/ca.crt
```

## 2. Untrusted CA Certificate

```
ldap.SERVER_DOWN: {'result': -1, 'desc': "Can't contact LDAP server", 'errno': 22, 'ctrls': [], 'info': '(unknown error code)'}
```

Remedy: Add to /etc/ldap/ldap.conf:

```
# TLS_CACERT  fully qualified path and filename of CA certificate file
# For example:
TLS_CACERT  /opt/symas/etc/openldap/certs/ca.crt
```

## 3. CA Certificate file not found

```
ldap.SERVER_DOWN: {'result': -1, 'desc': "Can't contact LDAP server", 'errno': 2, 'ctrls': [], 'info': 'No such file or directory'}
```

Remedy: Ensure cacert file pointed to by ldap.conf exists and is readable.

## 4. CA Certificate verification failed

```
ldap.SERVER_DOWN: {'result': -1, 'desc': "Can't contact LDAP server", 'ctrls': [], 'info': 'error:1416F086:SSL routines:tls_process_server_certificate:certificate verify failed (unable to get local issuer certificate)'}
```

Remedy: Ensure cacert file pointed to by ldap.conf exists and is readable.

## 5. CA Certificate verification failed hostname does not match

```
ldap.SERVER_DOWN: {'result': -1, 'desc': "Can't contact LDAP server", 'ctrls': [], 'info': 'TLS: hostname does not match subjectAltName in peer certificate'}
```

Remedy: Ensure the hostname specified in the uri matches the subject name of the CA certificate.

## 6. Err 107 Pointing to incorrect LDAP server

```
ldap.SERVER_DOWN: {'result': -1, 'desc': "Can't contact LDAP server", 'errno': 107, 'ctrls': [], 'info': 'Transport endpoint is not connected'}
```

Remedy: Ensure LDAP server is running and has the correct port in py-fortress-cfg.py

```python
# If not using LDAPS:
  "ldap": {
    "uri": "ldap://hostname:port",
    ...
  }
  
# OR If using LDAPS:
  "ldap": {
    "uri": "ldaps://hostname:port",
    ...
  }  
  ...
```

## 7. Unknown Error

```
ldap.SERVER_DOWN: {'result': -1, 'desc': "Can't contact LDAP server", 'ctrls': []}
```

Problem: Connecting to LDAPS port using ldap.  In the py-fortress-cfg.json:

```python
# Trying to connect to LDAPS port using without specifying ldaps on uri:
  "ldap": {
    "uri": "ldap://hostname:636",   <--- 636 is OpenLDAP's default ldaps port
    ...
  }
  ...
```

Remedy: When connecting to server over LDAPS port, be sure to specify ldaps in the uri:

```python
  "ldap": {
    "uri": "ldaps://hostname:636",   <--- 636 is OpenLDAP's default ldaps port, so use ldaps in uri
    ...
  }
  ...
```

## 8. Server is down or not listening on port specified

```
ldap.SERVER_DOWN: {'result': -1, 'desc': "Can't contact LDAP server", 'errno': 107, 'ctrls': [], 'info': 'Transport endpoint is not connected'}
```

Remedy: start the server

## 9. Incorrect DIT config

Occurs on routine updates:

```
ldap.NO_SUCH_OBJECT: {'msgtype': 101, 'msgid': 3, 'result': 32, 'desc': 'No such object', 'ctrls': [], 'info': "NO_SUCH_OBJECT: failed for MessageType : SEARCH_REQUEST\nMessage ID : 3\n    SearchRequest\n        baseDn : 'ou=
```

Remedy: Ensure the DIT exists and is specified correctly in the config:

```python
  "dit": {
    "suffix": "dc=example,dc=com",
    "users": "People",
    "roles": "Roles",
    "perms": "Perms"
  },
```

## 10. Incorrect rootdn config

Occurs on any operation:

```
ldap.INVALID_CREDENTIALS: {'msgtype': 97, 'msgid': 1, 'result': 49, 'desc': 'Invalid credentials', 'ctrls': [], 'info': 'INVALID_CREDENTIALS: Bind failed: ERR_229 Cannot authenticate user cn=manager,dc=example,dc=com'}
```

Remedy: Ensure the dn and password is specified correctly in the config:

```python
  "ldap": {
    ...
    "dn": "cn=manager,dc=example,dc=com",
    "password": "secret",
  },
 ```

## 11. Invalid runtime

Occurs when trying to run a test:

```
[root@72-14-182-7 py-fortress]# python3 rbac/tests/test_admin.py
Traceback (most recent call last):
  File "rbac/tests/test_admin.py", line 6, in <module>
    from rbac import admin, review
ModuleNotFoundError: No module named 'rbac'
```

Remedy: Did you prepare your terminal per [README-TESTING](./README-TESTING.md)?

________________________________________________________________________________
