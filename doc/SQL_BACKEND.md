# SQL Backend Configuration Guide

The py-fortress library now supports multiple data access backends: LDAP, file-based, and SQL databases.

## Configuration

To use the SQL backend, update your `py-fortress-cfg.json` configuration file:

```json
{
  "logger": {
    "level": "INFO",
    "file_name": "py-fortress",
    "console_out": true
  },
  "backend": "sql",
  "sql": {
    "driver": "sqlite3",
    "database": "/path/to/fortress.db",
    "host": "localhost",
    "port": 5432,
    "username": "fortress",
    "password": "secret"
  },
  "ldap": {
    "uri": "ldap://localhost:389",
    "timeout": 1,
    "pool_size": 5,
    "dn": "dc=example,dc=com",
    "password": "secret",
    "use_tls": false,
    "debug": false,
    "validate_cacert": true
  },
  "file": {
    "user": "/tmp/users.json",
    "role": "/tmp/roles.json", 
    "perm": "/tmp/perms.json"
  },
  "dit": {
    "suffix": "dc=example,dc=com",
    "users": "People",
    "roles": "Roles",
    "perms": "Perms"
  },
  "schema": {
    "raw_delimiter": "$"
  }
}
```

## Backend Options

Set the `backend` field to one of:

- `"ldap"` - Use LDAP directory (default)
- `"sql"` - Use SQL database
- `"file"` - Use JSON file storage

## SQL Configuration

Currently, only SQLite3 is supported:

```json
"sql": {
  "driver": "sqlite3",
  "database": "/path/to/fortress.db"
}
```

Future support for PostgreSQL and MySQL can be added by extending the `sqlhelper.py` module.

## Database Schema

The SQL backend automatically creates the following tables:

- `users` - User accounts and attributes
- `roles` - Role definitions 
- `perm_objects` - Permission objects
- `permissions` - Permissions and operations
- Relationships are stored as JSON arrays within the records

## Usage

No code changes are required! The admin API remains the same:

```python
from rbac import admin
from rbac.model import User, Role, Perm

# This will use whatever backend is configured
user = User(uid='testuser', password='secret123')
admin.add_user(user)

role = Role(name='testrole')
admin.add_role(role)

admin.assign(user, role)
```

## Switching Backends

You can switch backends by changing the configuration and restarting your application. The API signature remains identical across all backends.