"""
User Role Operations
"""

from database.db_config import (
    close_db_connection,
    commit_db_connection,
    get_db_connection,
)


def assign_role_to_user(user_id, role_id):
    """
    Assigns a role to a user.

    Args:
        user_id (int): User ID.
        role_id (int): Role ID.

    Returns:
        bool: True if assignment was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)", (user_id, role_id)
    )

    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0


def delete_user_roles_by_user(user_id):
    """
    Deletes all role assignments for a user.

    Args:
        user_id (int): User ID.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM user_roles WHERE user_id = ?", (user_id,))
    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0


def delete_user_roles_by_role(role_id):
    """
    Deletes all users assigned to a role.

    Args:
        role_id (int): Role ID.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM user_roles WHERE role_id = ?", (role_id,))
    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0
