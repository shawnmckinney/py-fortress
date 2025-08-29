'''
@copyright: 2022 - Symas Corporation
'''

import uuid
import json
from rbac.model import Perm, PermObj
from rbac.sql import sqlhelper
from rbac.sql.sqlex import NotFound, NotUnique, SqlException
from rbac.util import global_ids
from rbac.util.fortress_error import RbacError

def read(entity):
    """Read a single permission by obj_name and op_name"""
    permList = search(entity)
    if permList is None or len(permList) == 0:
        raise NotFound(msg="Perm Read not found, obj_name=" + entity.obj_name + ", op_name=" + entity.op_name, id=global_ids.PERM_NOT_FOUND)
    elif len(permList) > 1:
        raise NotUnique(msg="Perm Read not unique, obj_name=" + entity.obj_name + ", op_name=" + entity.op_name, id=global_ids.PERM_READ_FAILED)
    else:
        return permList[0]

def search(entity):
    """Search for permissions based on entity attributes"""
    query = "SELECT * FROM permissions WHERE 1=1"
    params = []
    
    if entity.obj_name:
        if '*' in entity.obj_name:
            query += " AND obj_name LIKE ?"
            params.append(entity.obj_name.replace('*', '%'))
        else:
            query += " AND obj_name = ?"
            params.append(entity.obj_name)
    
    if entity.op_name:
        if '*' in entity.op_name:
            query += " AND op_name LIKE ?"
            params.append(entity.op_name.replace('*', '%'))
        else:
            query += " AND op_name = ?"
            params.append(entity.op_name)
    
    if entity.obj_id:
        query += " AND obj_id = ?"
        params.append(entity.obj_id)
    
    try:
        rows = sqlhelper.execute_query(query, params)
        return [_unload(row) for row in rows]
    except Exception as e:
        raise RbacError(msg='Perm search failed, SQL error=' + str(e), id=global_ids.PERM_SEARCH_FAILED)

def search_on_roles(roles):
    """Search for permissions granted to specific roles"""
    if not roles:
        return []
    
    query = "SELECT * FROM permissions WHERE roles IS NOT NULL"
    
    try:
        rows = sqlhelper.execute_query(query)
        result = []
        for row in rows:
            perm_roles = json.loads(row['roles'] or '[]')
            if any(role in perm_roles for role in roles):
                result.append(_unload(row))
        return result
    except Exception as e:
        raise RbacError(msg='Perm search on roles failed, SQL error=' + str(e), id=global_ids.PERM_ROLE_SEARCH_FAILED)

def create(entity):
    """Create a new permission"""
    try:
        # Check if permission already exists
        existing = search(Perm(obj_name=entity.obj_name, op_name=entity.op_name))
        if existing:
            raise RbacError(msg='Perm create failed, already exists:' + entity.obj_name + ":" + entity.op_name, id=global_ids.PERM_ADD_FAILED)
    except NotFound:
        pass  # Good, permission doesn't exist
    
    # Generate internal ID if not provided
    if not entity.internal_id:
        entity.internal_id = str(uuid.uuid4())
    
    # Generate abstract name if not provided
    if not entity.abstract_name:
        entity.abstract_name = entity.obj_name + "." + entity.op_name
    
    query = """
        INSERT INTO permissions (
            obj_name, op_name, obj_id, internal_id, abstract_name, 
            description, type, props, roles
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    params = [
        entity.obj_name,
        entity.op_name,
        entity.obj_id,
        entity.internal_id,
        entity.abstract_name,
        entity.description,
        entity.type,
        json.dumps(entity.props) if entity.props else None,
        json.dumps(getattr(entity, 'roles', []))
    ]
    
    try:
        sqlhelper.execute_update(query, params)
        return entity
    except Exception as e:
        raise RbacError(msg='Perm create failed, obj_name=' + entity.obj_name + ', op_name=' + entity.op_name + ', SQL error=' + str(e), id=global_ids.PERM_ADD_FAILED)

def update(entity):
    """Update an existing permission"""
    # First check if permission exists
    existing = read(Perm(obj_name=entity.obj_name, op_name=entity.op_name))
    
    # Build dynamic update query based on provided fields
    updates = []
    params = []
    
    if entity.obj_id:
        updates.append("obj_id = ?")
        params.append(entity.obj_id)
    if entity.description:
        updates.append("description = ?")
        params.append(entity.description)
    if entity.type:
        updates.append("type = ?")
        params.append(entity.type)
    if entity.props is not None:
        updates.append("props = ?")
        params.append(json.dumps(entity.props) if entity.props else None)
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        query = f"UPDATE permissions SET {', '.join(updates)} WHERE obj_name = ? AND op_name = ?"
        params.extend([entity.obj_name, entity.op_name])
        
        try:
            sqlhelper.execute_update(query, params)
            return entity
        except Exception as e:
            raise RbacError(msg='Perm update failed, obj_name=' + entity.obj_name + ', op_name=' + entity.op_name + ', SQL error=' + str(e), id=global_ids.PERM_UPDATE_FAILED)
    
    return entity

def delete(entity):
    """Delete a permission"""
    # Check if permission exists first
    existing = read(Perm(obj_name=entity.obj_name, op_name=entity.op_name))
    
    query = "DELETE FROM permissions WHERE obj_name = ? AND op_name = ?"
    try:
        rowcount = sqlhelper.execute_update(query, [entity.obj_name, entity.op_name])
        if rowcount == 0:
            raise NotFound(msg='Perm delete not found:' + entity.obj_name + ":" + entity.op_name, id=global_ids.PERM_NOT_FOUND)
        return entity
    except NotFound:
        raise
    except Exception as e:
        raise RbacError(msg='Perm delete failed, obj_name=' + entity.obj_name + ', op_name=' + entity.op_name + ', SQL error=' + str(e), id=global_ids.PERM_DELETE_FAILED)

def grant(entity, role):
    """Grant a permission to a role"""
    perm = read(Perm(obj_name=entity.obj_name, op_name=entity.op_name))
    roles = json.loads(perm.roles or '[]') if hasattr(perm, 'roles') and perm.roles else []
    
    role_name = role.name if hasattr(role, 'name') else str(role)
    if role_name not in roles:
        roles.append(role_name)
        query = "UPDATE permissions SET roles = ?, updated_at = CURRENT_TIMESTAMP WHERE obj_name = ? AND op_name = ?"
        try:
            sqlhelper.execute_update(query, [json.dumps(roles), entity.obj_name, entity.op_name])
        except Exception as e:
            raise RbacError(msg='Perm grant failed, obj_name=' + entity.obj_name + ', op_name=' + entity.op_name + ', role=' + role_name + ', SQL error=' + str(e), id=global_ids.PERM_GRANT_FAILED)

def revoke(entity, role):
    """Revoke a permission from a role"""
    perm = read(Perm(obj_name=entity.obj_name, op_name=entity.op_name))
    roles = json.loads(perm.roles or '[]') if hasattr(perm, 'roles') and perm.roles else []
    
    role_name = role.name if hasattr(role, 'name') else str(role)
    if role_name in roles:
        roles.remove(role_name)
        query = "UPDATE permissions SET roles = ?, updated_at = CURRENT_TIMESTAMP WHERE obj_name = ? AND op_name = ?"
        try:
            sqlhelper.execute_update(query, [json.dumps(roles), entity.obj_name, entity.op_name])
        except Exception as e:
            raise RbacError(msg='Perm revoke failed, obj_name=' + entity.obj_name + ', op_name=' + entity.op_name + ', role=' + role_name + ', SQL error=' + str(e), id=global_ids.PERM_REVOKE_FAILED)

# Permission Object operations

def read_obj(entity):
    """Read a single permission object by obj_name"""
    objList = search_objs(entity)
    if objList is None or len(objList) == 0:
        raise NotFound(msg="PermObj Read not found, obj_name=" + entity.obj_name, id=global_ids.PERM_OBJ_NOT_FOUND)
    elif len(objList) > 1:
        raise NotUnique(msg="PermObj Read not unique, obj_name=" + entity.obj_name, id=global_ids.PERM_OBJ_READ_FAILED)
    else:
        return objList[0]

def search_objs(entity):
    """Search for permission objects"""
    query = "SELECT * FROM perm_objects WHERE 1=1"
    params = []
    
    if entity.obj_name:
        if '*' in entity.obj_name:
            query += " AND obj_name LIKE ?"
            params.append(entity.obj_name.replace('*', '%'))
        else:
            query += " AND obj_name = ?"
            params.append(entity.obj_name)
    
    if hasattr(entity, 'obj_id') and entity.obj_id:
        query += " AND obj_id = ?"
        params.append(entity.obj_id)
    
    try:
        rows = sqlhelper.execute_query(query, params)
        return [_unload_obj(row) for row in rows]
    except Exception as e:
        raise RbacError(msg='PermObj search failed, SQL error=' + str(e), id=global_ids.PERM_OBJ_SEARCH_FAILED)

def create_obj(entity):
    """Create a new permission object"""
    try:
        # Check if permission object already exists
        existing = search_objs(PermObj(obj_name=entity.obj_name))
        if existing:
            raise RbacError(msg='PermObj create failed, already exists:' + entity.obj_name, id=global_ids.PERM_OBJ_ADD_FAILED)
    except NotFound:
        pass  # Good, object doesn't exist
    
    # Generate internal ID if not provided
    if not entity.internal_id:
        entity.internal_id = str(uuid.uuid4())
    
    query = """
        INSERT INTO perm_objects (obj_name, obj_id, internal_id, description, ou, type, props)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    
    params = [
        entity.obj_name,
        getattr(entity, 'obj_id', None),
        entity.internal_id,
        entity.description,
        entity.ou,
        entity.type,
        json.dumps(entity.props) if entity.props else None
    ]
    
    try:
        sqlhelper.execute_update(query, params)
        return entity
    except Exception as e:
        raise RbacError(msg='PermObj create failed, obj_name=' + entity.obj_name + ', SQL error=' + str(e), id=global_ids.PERM_OBJ_ADD_FAILED)

def update_obj(entity):
    """Update an existing permission object"""
    # First check if object exists
    existing = read_obj(PermObj(obj_name=entity.obj_name))
    
    # Build dynamic update query based on provided fields
    updates = []
    params = []
    
    if hasattr(entity, 'obj_id') and entity.obj_id:
        updates.append("obj_id = ?")
        params.append(entity.obj_id)
    if entity.description:
        updates.append("description = ?")
        params.append(entity.description)
    if entity.ou:
        updates.append("ou = ?")
        params.append(entity.ou)
    if entity.type:
        updates.append("type = ?")
        params.append(entity.type)
    if entity.props is not None:
        updates.append("props = ?")
        params.append(json.dumps(entity.props) if entity.props else None)
    
    if updates:
        updates.append("updated_at = CURRENT_TIMESTAMP")
        query = f"UPDATE perm_objects SET {', '.join(updates)} WHERE obj_name = ?"
        params.append(entity.obj_name)
        
        try:
            sqlhelper.execute_update(query, params)
            return entity
        except Exception as e:
            raise RbacError(msg='PermObj update failed, obj_name=' + entity.obj_name + ', SQL error=' + str(e), id=global_ids.PERM_OBJ_UPDATE_FAILED)
    
    return entity

def delete_obj(entity):
    """Delete a permission object"""
    # Check if object exists first
    existing = read_obj(PermObj(obj_name=entity.obj_name))
    
    query = "DELETE FROM perm_objects WHERE obj_name = ?"
    try:
        rowcount = sqlhelper.execute_update(query, [entity.obj_name])
        if rowcount == 0:
            raise NotFound(msg='PermObj delete not found:' + entity.obj_name, id=global_ids.PERM_OBJ_NOT_FOUND)
        return entity
    except NotFound:
        raise
    except Exception as e:
        raise RbacError(msg='PermObj delete failed, obj_name=' + entity.obj_name + ', SQL error=' + str(e), id=global_ids.PERM_OBJ_DELETE_FAILED)

def _unload(row):
    """Convert database row to Perm object"""
    entity = Perm()
    entity.obj_name = row['obj_name']
    entity.op_name = row['op_name']
    entity.obj_id = row['obj_id']
    entity.internal_id = row['internal_id']
    entity.abstract_name = row['abstract_name']
    entity.description = row['description']
    entity.type = row['type']
    
    # Parse JSON fields
    if row['props']:
        entity.props = json.loads(row['props'])
    if row['roles']:
        entity.roles = json.loads(row['roles'])
    
    return entity

def _unload_obj(row):
    """Convert database row to PermObj object"""
    entity = PermObj()
    entity.obj_name = row['obj_name']
    if row['obj_id']:
        entity.obj_id = row['obj_id']
    entity.internal_id = row['internal_id']
    entity.description = row['description']
    entity.ou = row['ou']
    entity.type = row['type']
    
    # Parse JSON fields
    if row['props']:
        entity.props = json.loads(row['props'])
    
    return entity