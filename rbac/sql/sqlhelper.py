'''
@copyright: 2022 - Symas Corporation
'''

import sqlite3
import threading
from rbac.util import Config
from rbac.util import logger
from rbac.sql.sqlex import SqlException
from rbac.util import global_ids

# Thread-local storage for connections
_local = threading.local()

def get_connection():
    """
    Get a database connection from thread-local storage or create one
    """
    if not hasattr(_local, 'conn'):
        sql_config = Config.get('sql')
        driver = sql_config.get('driver', 'sqlite3')
        
        if driver == 'sqlite3':
            database = sql_config.get('database', '/tmp/fortress.db')
            _local.conn = sqlite3.connect(database)
            _local.conn.row_factory = sqlite3.Row  # Enable column access by name
        else:
            # For other databases like PostgreSQL, MySQL, etc.
            raise SqlException(msg=f"Database driver {driver} not yet supported", id=global_ids.CONFIG_BOOTSTRAP_FAILED)
    
    return _local.conn

def close_connection():
    """
    Close the thread-local database connection
    """
    if hasattr(_local, 'conn'):
        _local.conn.close()
        del _local.conn

def execute_query(query, params=None):
    """
    Execute a query and return results
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"SQL query failed: {query}, params: {params}, error: {e}")
        raise SqlException(msg=f"SQL query failed: {e}", id=global_ids.SQL_EXEC_FAILED)

def execute_update(query, params=None):
    """
    Execute an update/insert/delete query and commit
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        conn.rollback()
        logger.error(f"SQL update failed: {query}, params: {params}, error: {e}")
        raise SqlException(msg=f"SQL update failed: {e}", id=global_ids.SQL_EXEC_FAILED)

def init_schema():
    """
    Initialize the database schema if it doesn't exist
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY,
            internal_id TEXT,
            cn TEXT,
            sn TEXT,
            password TEXT,
            description TEXT,
            ou TEXT,
            display_name TEXT,
            employee_type TEXT,
            title TEXT,
            department_number TEXT,
            l TEXT,
            physical_delivery_office_name TEXT,
            postal_code TEXT,
            room_number TEXT,
            pw_policy TEXT,
            system INTEGER DEFAULT 0,
            phones TEXT,  -- JSON array
            mobiles TEXT,  -- JSON array
            emails TEXT,  -- JSON array
            props TEXT,   -- JSON array
            constraint_data TEXT,  -- JSON constraint
            roles TEXT,   -- JSON array of roles
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Roles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            name TEXT PRIMARY KEY,
            internal_id TEXT,
            description TEXT,
            props TEXT,  -- JSON array
            constraint_data TEXT,  -- JSON constraint
            members TEXT,  -- JSON array of members
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Permission objects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS perm_objects (
            obj_name TEXT PRIMARY KEY,
            obj_id TEXT,
            internal_id TEXT,
            description TEXT,
            ou TEXT,
            type TEXT,
            props TEXT,  -- JSON array
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Permissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            obj_name TEXT,
            op_name TEXT,
            obj_id TEXT,
            internal_id TEXT,
            abstract_name TEXT,
            description TEXT,
            type TEXT,
            props TEXT,  -- JSON array
            roles TEXT,  -- JSON array of granted roles
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(obj_name, op_name),
            FOREIGN KEY (obj_name) REFERENCES perm_objects (obj_name)
        )
    ''')
    
    conn.commit()

# Initialize schema on module load
try:
    init_schema()
except Exception as e:
    logger.warning(f"Failed to initialize SQL schema: {e}")