# pylint: disable=R0801
"""
Permission Operations
"""

from database.db_config import (
    close_db_connection,
    commit_db_connection,
    get_db_connection,
)

from .role_permissions_ops import delete_role_permissions_by_permission


def create_permission(name, description=None):
    """
    Creates a new permission.

    Args:
        name (str): Permission name.
        description (str, optional): Permission description.

    Returns:
        int: The ID of the newly created permission.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO permissions (name, description) VALUES (?, ?)", (name, description)
    )

    permission_id = cursor.lastrowid
    commit_db_connection(connection)
    close_db_connection(connection)

    return permission_id


def delete_permission(permission_id):
    """
    Deletes a permission and its related records.

    Args:
        permission_id (int): Permission ID.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    connection = get_db_connection()

    delete_role_permissions_by_permission(permission_id)

    cursor = connection.cursor()
    cursor.execute("DELETE FROM permissions WHERE id = ?", (permission_id,))
    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0
