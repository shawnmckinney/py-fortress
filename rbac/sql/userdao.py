'''
@copyright: 2022 - Symas Corporation
'''

import uuid
import json
import hashlib
from rbac.model import User, Constraint
from rbac.sql import sqlhelper
from rbac.sql.sqlex import NotFound, NotUnique, InvalidCredentials, SqlException
from rbac.util import global_ids
from rbac.util.fortress_error import RbacError

def read(entity):
    """Read a single user by uid"""
    userList = search(entity)
    if userList is None or len(userList) == 0:
        raise NotFound(msg="User Read not found, uid=" + entity.uid, id=global_ids.USER_NOT_FOUND)
    elif len(userList) > 1:
        raise NotUnique(msg="User Read not unique, uid=" + entity.uid, id=global_ids.USER_READ_FAILED)
    else:
        return userList[0]

def authenticate(entity):
    """Authenticate a user with uid and password"""
    try:
        user = read(entity)
        if not user.password or not entity.password:
            raise InvalidCredentials(msg="Authentication failed for uid=" + entity.uid, id=global_ids.USER_PW_CHK_FAILED)
        
        # Simple hash comparison - in production, use proper password hashing
        hashed_password = hashlib.sha256(entity.password.encode()).hexdigest()
        if user.password != hashed_password:
            raise InvalidCredentials(msg="Authentication failed for uid=" + entity.uid, id=global_ids.USER_PW_CHK_FAILED)
        
        return True
    except (NotFound, NotUnique, InvalidCredentials):
        raise InvalidCredentials(msg="Authentication failed for uid=" + entity.uid, id=global_ids.USER_PW_CHK_FAILED)
    except Exception as e:
        raise RbacError(msg='User Authenticate error for uid=' + entity.uid + ', SQL error=' + str(e), id=global_ids.USER_PW_CHK_FAILED)

def search(entity):
    """Search for users based on entity attributes"""
    query = "SELECT * FROM users WHERE 1=1"
    params = []
    
    if entity.uid:
        if '*' in entity.uid:
            query += " AND uid LIKE ?"
            params.append(entity.uid.replace('*', '%'))
        else:
            query += " AND uid = ?"
            params.append(entity.uid)
    
    if entity.ou:
        query += " AND ou = ?"
        params.append(entity.ou)
    
    try:
        rows = sqlhelper.execute_query(query, params)
        return [_unload(row) for row in rows]
    except Exception as e:
        raise RbacError(msg='User search failed, SQL error=' + str(e), id=global_ids.USER_SEARCH_FAILED)

def search_on_roles(roles):
    """Search for users who have specific roles"""
    if not roles:
        return []
    
    # Build a query to find users who have any of the specified roles
    placeholders = ','.join(['?' for _ in roles])
    query = f"SELECT * FROM users WHERE roles IS NOT NULL"
    
    try:
        rows = sqlhelper.execute_query(query)
        result = []
        for row in rows:
            user_roles = json.loads(row['roles'] or '[]')
            if any(role in user_roles for role in roles):
                result.append(_unload(row))
        return result
    except Exception as e:
        raise RbacError(msg='User search on roles failed, SQL error=' + str(e), id=global_ids.USER_SEARCH_FAILED)

def create(entity):
    """Create a new user"""
    try:
        # Check if user already exists
        existing = search(User(uid=entity.uid))
        if existing:
            raise RbacError(msg='User create failed, already exists:' + entity.uid, id=global_ids.USER_ADD_FAILED)
    except NotFound:
        pass  # Good, user doesn't exist
    
    # Generate internal ID if not provided
    if not entity.internal_id:
        entity.internal_id = str(uuid.uuid4())
    
    # Set defaults
    if not entity.cn:
        entity.cn = entity.uid
    if not entity.sn:
        entity.sn = entity.uid
    
    # Hash password
    hashed_password = None
    if entity.password:
        hashed_password = hashlib.sha256(entity.password.encode()).hexdigest()
    
    query = """
        INSERT INTO users (
            uid, internal_id, cn, sn, password, description, ou, display_name,
            employee_type, title, department_number, l, physical_delivery_office_name,
            postal_code, room_number, pw_policy, system, phones, mobiles, emails,
            props, constraint_data, roles
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    params = [
        entity.uid,
        entity.internal_id,
        entity.cn,
        entity.sn,
        hashed_password,
        entity.description,
        entity.ou,
        entity.display_name,
        entity.employee_type,
        entity.title,
        entity.department_number,
        getattr(entity, 'l', None),
        entity.physical_delivery_office_name,
        entity.postal_code,
        entity.room_number,
        entity.pw_policy,
        1 if entity.system else 0,
        json.dumps(entity.phones) if entity.phones else None,
        json.dumps(entity.mobiles) if entity.mobiles else None,
        json.dumps(entity.emails) if entity.emails else None,
        json.dumps(entity.props) if entity.props else None,
        entity.constraint.get_raw() if entity.constraint else None,
        json.dumps(getattr(entity, 'roles', [])) if hasattr(entity, 'roles') and entity.roles else json.dumps([])
    ]
    
    try:
        sqlhelper.execute_update(query, params)
        return entity
    except Exception as e:
        raise RbacError(msg='User create failed, uid=' + entity.uid + ', SQL error=' + str(e), id=global_ids.USER_ADD_FAILED)

def update(entity):
    """Update an existing user"""
    # First check if user exists
    existing = read(User(uid=entity.uid))
    
    # Build dynamic update query based on provided fields
    updates = []
    params = []
    
    if entity.cn:
        updates.append("cn = ?")
        params.append(entity.cn)
    if entity.sn:
        updates.append("sn = ?")
        params.append(entity.sn)
    if entity.password:
        updates.append("password = ?")
        params.append(hashlib.sha256(entity.password.encode()).hexdigest())
    if entity.description:
        updates.append("description = ?")
        params.append(entity.description)
    if entity.ou:
        updates.append("ou = ?")
        params.append(entity.ou)
    if entity.display_name:
        updates.append("display_name = ?")
        params.append(entity.display_name)
    if entity.employee_type:
        updates.append("employee_type = ?")
        params.append(entity.employee_type)
    if entity.title:
        updates.append("title = ?")
        params.append(entity.title)
    if entity.department_number:
        updates.append("department_number = ?")
        params.append(entity.department_number)
    if hasattr(entity, 'l') and entity.l:
        updates.append("l = ?")
        params.append(entity.l)
    if entity.physical_delivery_office_name:
        updates.append("physical_delivery_office_name = ?")
        params.append(entity.physical_delivery_office_name)
    if entity.postal_code:
        updates.append("postal_code = ?")
        params.append(entity.postal_code)
    if entity.room_number:
        updates.append("room_number = ?")
        params.append(entity.room_number)
    if entity.pw_policy:
        updates.append("pw_policy = ?")
        params.append(entity.pw_policy)
    if entity.system is not None:
        updates.append("system = ?")
        params.append(1 if entity.system else 0)
    if entity.phones is not None:
        updates.append("phones = ?")
        params.append(json.dumps(entity.phones) if entity.phones else None)
    if entity.mobiles is not None:
        updates.append("mobiles = ?")
        params.append(json.dumps(entity.mobiles) if entity.mobiles else None)
    if entity.emails is not None:
        updates.append("emails = ?")
        params.append(json.dumps(entity.emails) if entity.emails else None)
    if entity.props is not None:
        updates.append("props = ?")
        params.append(json.dumps(entity.props) if entity.props else None)
    if entity.constraint is not None:
        updates.append("constraint_data = ?")
        params.append(entity.constraint.get_raw())
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        query = f"UPDATE users SET {', '.join(updates)} WHERE uid = ?"
        params.append(entity.uid)
        
        try:
            sqlhelper.execute_update(query, params)
            return entity
        except Exception as e:
            raise RbacError(msg='User update failed, uid=' + entity.uid + ', SQL error=' + str(e), id=global_ids.USER_UPDATE_FAILED)
    
    return entity

def delete(entity):
    """Delete a user"""
    # Check if user exists first
    existing = read(User(uid=entity.uid))
    
    query = "DELETE FROM users WHERE uid = ?"
    try:
        rowcount = sqlhelper.execute_update(query, [entity.uid])
        if rowcount == 0:
            raise NotFound(msg='User delete failed, not found:' + entity.uid, id=global_ids.USER_NOT_FOUND)
        return entity
    except NotFound:
        raise
    except Exception as e:
        raise RbacError(msg='User delete failed, uid=' + entity.uid + ', SQL error=' + str(e), id=global_ids.USER_DELETE_FAILED)

def assign(entity, constraint):
    """Assign a role to a user"""
    user = read(User(uid=entity.uid))
    roles = json.loads(user.roles or '[]') if hasattr(user, 'roles') and user.roles else []
    
    # Store the role name, not the constraint object
    role_name = constraint.name if hasattr(constraint, 'name') else str(constraint)
    if role_name not in roles:
        roles.append(role_name)
        query = "UPDATE users SET roles = ?, updated_at = CURRENT_TIMESTAMP WHERE uid = ?"
        try:
            sqlhelper.execute_update(query, [json.dumps(roles), entity.uid])
        except Exception as e:
            raise RbacError(msg='User role assignment failed, uid=' + entity.uid + ', SQL error=' + str(e), id=global_ids.URLE_ASSIGN_FAILED)

def deassign(entity, constraint):
    """Remove a role from a user"""
    user = read(User(uid=entity.uid))
    roles = json.loads(user.roles or '[]') if hasattr(user, 'roles') and user.roles else []
    
    # Remove the role name
    role_name = constraint.name if hasattr(constraint, 'name') else str(constraint)
    if role_name in roles:
        roles.remove(role_name)
        query = "UPDATE users SET roles = ?, updated_at = CURRENT_TIMESTAMP WHERE uid = ?"
        try:
            sqlhelper.execute_update(query, [json.dumps(roles), entity.uid])
        except Exception as e:
            raise RbacError(msg='User role deassignment failed, uid=' + entity.uid + ', SQL error=' + str(e), id=global_ids.URLE_DEASSIGN_FAILED)

def _unload(row):
    """Convert database row to User object"""
    entity = User()
    entity.uid = row['uid']
    entity.internal_id = row['internal_id']
    entity.cn = row['cn']
    entity.sn = row['sn']
    entity.password = row['password']
    entity.description = row['description']
    entity.ou = row['ou']
    entity.display_name = row['display_name']
    entity.employee_type = row['employee_type']
    entity.title = row['title']
    entity.department_number = row['department_number']
    entity.l = row['l']
    entity.physical_delivery_office_name = row['physical_delivery_office_name']
    entity.postal_code = row['postal_code']
    entity.room_number = row['room_number']
    entity.pw_policy = row['pw_policy']
    entity.system = bool(row['system'])
    
    # Parse JSON fields
    if row['phones']:
        entity.phones = json.loads(row['phones'])
    if row['mobiles']:
        entity.mobiles = json.loads(row['mobiles'])
    if row['emails']:
        entity.emails = json.loads(row['emails'])
    if row['props']:
        entity.props = json.loads(row['props'])
    
    # Handle roles - ensure it's always a list
    if row['roles']:
        roles_data = json.loads(row['roles'])
        entity.roles = roles_data if roles_data is not None else []
    else:
        entity.roles = []  # Always provide an empty list if no roles
    
    # Initialize role_constraints as empty list (like LDAP version does)
    entity.role_constraints = []
        
    if row['constraint_data']:
        entity.constraint = Constraint(raw=row['constraint_data'])
    else:
        # Always create a constraint, even if empty (like LDAP version does)
        entity.constraint = Constraint()
    
    return entity