'''
@copyright: 2022 - Symas Corporation
'''

import uuid
import json
from rbac.model import Role, Constraint
from rbac.sql import sqlhelper
from rbac.sql.sqlex import NotFound, NotUnique, SqlException
from rbac.util import global_ids
from rbac.util.fortress_error import RbacError

def read(entity):
    """Read a single role by name"""
    roleList = search(entity)
    if roleList is None or len(roleList) == 0:
        raise NotFound(msg="Role Read not found, name=" + entity.name, id=global_ids.ROLE_NOT_FOUND)
    elif len(roleList) > 1:
        raise NotUnique(msg="Role Read not unique, name=" + entity.name, id=global_ids.ROLE_READ_FAILED)
    else:
        return roleList[0]

def search(entity):
    """Search for roles based on entity attributes"""
    query = "SELECT * FROM roles WHERE 1=1"
    params = []
    
    if entity.name:
        if '*' in entity.name:
            query += " AND name LIKE ?"
            params.append(entity.name.replace('*', '%'))
        else:
            query += " AND name = ?"
            params.append(entity.name)
    
    if entity.description:
        query += " AND description LIKE ?"
        params.append('%' + entity.description + '%')
    
    try:
        rows = sqlhelper.execute_query(query, params)
        return [_unload(row) for row in rows]
    except Exception as e:
        raise RbacError(msg='Role search failed, SQL error=' + str(e), id=global_ids.ROLE_SEARCH_FAILED)

def create(entity):
    """Create a new role"""
    try:
        # Check if role already exists
        existing = search(Role(name=entity.name))
        if existing:
            raise RbacError(msg='Role create failed, already exists:' + entity.name, id=global_ids.ROLE_ADD_FAILED)
    except NotFound:
        pass  # Good, role doesn't exist
    
    # Generate internal ID if not provided
    if not entity.internal_id:
        entity.internal_id = str(uuid.uuid4())
    
    # Set default constraint if not provided
    if not entity.constraint:
        entity.constraint = Constraint(name=entity.name)
    
    query = """
        INSERT INTO roles (name, internal_id, description, props, constraint_data, members)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    
    params = [
        entity.name,
        entity.internal_id,
        entity.description,
        json.dumps(entity.props) if entity.props else None,
        entity.constraint.get_raw() if entity.constraint else None,
        json.dumps(getattr(entity, 'members', []))
    ]
    
    try:
        sqlhelper.execute_update(query, params)
        return entity
    except Exception as e:
        raise RbacError(msg='Role create failed, name=' + entity.name + ', SQL error=' + str(e), id=global_ids.ROLE_ADD_FAILED)

def update(entity):
    """Update an existing role"""
    # First check if role exists
    existing = read(Role(name=entity.name))
    
    # Build dynamic update query based on provided fields
    updates = []
    params = []
    
    if entity.description:
        updates.append("description = ?")
        params.append(entity.description)
    if entity.props is not None:
        updates.append("props = ?")
        params.append(json.dumps(entity.props) if entity.props else None)
    if entity.constraint is not None:
        updates.append("constraint_data = ?")
        params.append(entity.constraint.get_raw())
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        query = f"UPDATE roles SET {', '.join(updates)} WHERE name = ?"
        params.append(entity.name)
        
        try:
            sqlhelper.execute_update(query, params)
            return entity
        except Exception as e:
            raise RbacError(msg='Role update failed, name=' + entity.name + ', SQL error=' + str(e), id=global_ids.ROLE_UPDATE_FAILED)
    
    return entity

def delete(entity):
    """Delete a role"""
    # Check if role exists first
    existing = read(Role(name=entity.name))
    
    query = "DELETE FROM roles WHERE name = ?"
    try:
        rowcount = sqlhelper.execute_update(query, [entity.name])
        if rowcount == 0:
            raise NotFound(msg='Role delete not found:' + entity.name, id=global_ids.ROLE_NOT_FOUND)
        return entity
    except NotFound:
        raise
    except Exception as e:
        raise RbacError(msg='Role delete failed, name=' + entity.name + ', SQL error=' + str(e), id=global_ids.ROLE_DELETE_FAILED)

def add_member(entity, uid):
    """Add a user as a member of this role"""
    role = read(Role(name=entity.name))
    members = json.loads(role.members or '[]') if hasattr(role, 'members') and role.members else []
    
    if uid not in members:
        members.append(uid)
        query = "UPDATE roles SET members = ?, updated_at = CURRENT_TIMESTAMP WHERE name = ?"
        try:
            sqlhelper.execute_update(query, [json.dumps(members), entity.name])
        except Exception as e:
            raise RbacError(msg='Role add member failed, name=' + entity.name + ', uid=' + uid + ', SQL error=' + str(e), id=global_ids.ROLE_OCCUPANT_FAILED)

def remove_member(entity, uid):
    """Remove a user as a member of this role"""
    role = read(Role(name=entity.name))
    members = json.loads(role.members or '[]') if hasattr(role, 'members') and role.members else []
    
    if uid in members:
        members.remove(uid)
        query = "UPDATE roles SET members = ?, updated_at = CURRENT_TIMESTAMP WHERE name = ?"
        try:
            sqlhelper.execute_update(query, [json.dumps(members), entity.name])
        except Exception as e:
            raise RbacError(msg='Role remove member failed, name=' + entity.name + ', uid=' + uid + ', SQL error=' + str(e), id=global_ids.ROLE_REMOVE_OCCUPANT_FAILED)

def get_members(entity):
    """Get all members (users) of this role"""
    role = read(Role(name=entity.name))
    members = json.loads(role.members or '[]') if hasattr(role, 'members') and role.members else []
    return members

def get_members_constraint(entity):
    """Get all members with their constraints - for now just return members"""
    # This would typically return members with their role constraints
    # For simplicity, returning just the members list
    return get_members(entity)

def _unload(row):
    """Convert database row to Role object"""
    entity = Role()
    entity.name = row['name']
    entity.internal_id = row['internal_id']
    entity.description = row['description']
    
    # Parse JSON fields
    if row['props']:
        entity.props = json.loads(row['props'])
    if row['members']:
        entity.members = json.loads(row['members'])
    if row['constraint_data']:
        # Create constraint from raw data
        entity.constraint = Constraint(raw=row['constraint_data'])
    
    return entity