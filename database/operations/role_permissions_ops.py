# pylint: disable=R0801
"""
Role Permission Operations
"""

from database.db_config import (
    close_db_connection,
    commit_db_connection,
    get_db_connection,
)


def assign_permission_to_role(role_id, permission_id):
    """
    Assigns a permission to a role.

    Args:
        role_id (int): Role ID.
        permission_id (int): Permission ID.

    Returns:
        bool: True if assignment was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO role_permissions (role_id, permission_id) VALUES (?, ?)",
        (role_id, permission_id),
    )

    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0


def delete_role_permissions_by_role(role_id):
    """
    Deletes all permissions assigned to a role.

    Args:
        role_id (int): Role ID.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM role_permissions WHERE role_id = ?", (role_id,))
    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0


def delete_role_permissions_by_permission(permission_id):
    """
    Deletes all roles assigned to a permission.

    Args:
        permission_id (int): Permission ID.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM role_permissions WHERE permission_id = ?", (permission_id,)
    )
    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0
