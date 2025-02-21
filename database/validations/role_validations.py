# app/validations/role_validations.py

# This file contains functional validation functions for role-related operations.
# These functions check the business rules, such as role name validity, and role existence.

from database.exceptions.validation_exceptions import (
    InvalidRoleNameError,
    RoleNotFoundError,
)
from database.operations.roles_ops import get_role_by_id


def validate_role_name(name: str):
    """
    Validate the role name according to business rules.

    Args:
        name (str): The name of the role.

    Raises:
        InvalidRoleNameError: If the role name is empty or doesn't meet the business rules.

    Returns:
        bool: True if the role name is valid.
    """
    if not name.strip():
        raise InvalidRoleNameError(message="Role name is required.")
    if len(name) < 3:
        raise InvalidRoleNameError(
            message="Role name must be at least 3 characters long."
        )
    return True


def validate_role_existence(role_id: int):
    """
    Validate if a role exists in the database.

    Args:
        role_id (int): The ID of the role to check.

    Raises:
        RoleNotFoundError: If the role does not exist.

    Returns:
        bool: True if the role exists.
    """
    # Call the operation to retrieve the role by ID
    role = get_role_by_id(role_id)

    if not role:
        raise RoleNotFoundError(message="Role not found.")
    return True
