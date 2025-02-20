"""
Role Operations
"""

from .role_permissions_ops import delete_role_permissions_by_role
from .user_roles_ops import delete_user_roles_by_role

from database.db_config import (
    close_db_connection,
    commit_db_connection,
    get_db_connection,
)


def create_role(name, description=None):
    """
    Creates a new role.

    Args:
        name (str): Role name.
        description (str, optional): Role description.

    Returns:
        int: The ID of the newly created role.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO roles (name, description) VALUES (?, ?)", (name, description)
    )

    role_id = cursor.lastrowid
    commit_db_connection(connection)
    close_db_connection(connection)

    return role_id


def delete_role(role_id):
    """
    Deletes a role and its related records.

    Args:
        role_id (int): Role ID.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    connection = get_db_connection()

    delete_user_roles_by_role(role_id)
    delete_role_permissions_by_role(role_id)

    cursor = connection.cursor()
    cursor.execute("DELETE FROM roles WHERE id = ?", (role_id,))
    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0
