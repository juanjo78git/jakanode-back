# pylint: disable=R0801
"""
Role Operations
"""

from database.db_config import (
    close_db_connection,
    commit_db_connection,
    get_db_connection,
)
from database.models.roles import format_role_data
from database.validations.role_validations import (
    validate_role_existence,
    validate_role_name,
)

from .role_permissions_ops import delete_role_permissions_by_role
from .user_roles_ops import delete_user_roles_by_role


def create_role(name, description=None):
    """
    Creates a new role.

    Args:
        name (str): Role name.
        description (str, optional): Role description.

    Returns:
        int: The ID of the newly created role.
    """
    # Validate the role name before creating it
    validate_role_name(name)

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO roles (name, description) VALUES (?, ?)", (name, description)
    )

    role_id = cursor.lastrowid
    commit_db_connection(connection)
    close_db_connection(connection)

    return role_id


def update_role(role_id, name=None, description=None):
    """
    Updates an existing role with new name and/or description.

    Args:
        role_id (int): The ID of the role to update.
        name (str, optional): New role name.
        description (str, optional): New role description.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    # Validate that the role exists before updating it
    validate_role_existence(role_id)

    # Validate the new role name if provided
    if name:
        validate_role_name(name)

    connection = get_db_connection()
    cursor = connection.cursor()

    # Update the role name and/or description
    if name:
        cursor.execute("UPDATE roles SET name = ? WHERE id = ?", (name, role_id))
    if description:
        cursor.execute(
            "UPDATE roles SET description = ? WHERE id = ?", (description, role_id)
        )

    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0


def delete_role(role_id):
    """
    Deletes a role and its related records.

    Args:
        role_id (int): Role ID.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    # Validate that the role exists before attempting deletion
    validate_role_existence(role_id)

    connection = get_db_connection()

    delete_user_roles_by_role(role_id)
    delete_role_permissions_by_role(role_id)

    cursor = connection.cursor()
    cursor.execute("DELETE FROM roles WHERE id = ?", (role_id,))
    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0


def get_role_by_id(role_id):
    """
    Retrieves a role by its ID.

    Args:
        role_id (int): The ID of the role to retrieve.

    Returns:
        dict: A dictionary containing the role's data, or None if not found.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM roles WHERE id = ?", (role_id,))
    role_data = cursor.fetchone()

    role = format_role_data(role_data)

    close_db_connection(connection)

    return role


def get_all_roles():
    """
    Retrieves a list of all roles in the system.

    Returns:
        list: A list of dictionaries, each containing a role's data.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM roles")
    roles_data = cursor.fetchall()

    roles = [format_role_data(role) for role in roles_data]

    close_db_connection(connection)

    return roles
