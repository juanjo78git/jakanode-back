"""
User with Roles and Permissions Model
"""

from database.models.users import format_user_data
from database.models.roles import format_role_data
from database.models.permissions import format_permission_data

def format_user_with_roles_permissions(user_data, roles_data, permissions_data):
    """
    Formats user data including their roles and permissions.

    Args:
        user_data (tuple): User data from the database.
        roles_data (list of tuples): List of roles assigned to the user.
        permissions_data (list of tuples): List of permissions derived from roles.

    Returns:
        dict: A dictionary containing user data, roles, and permissions.
    """
    if user_data:
        return {
            "user": format_user_data(user_data),
            "roles": [format_role_data(role) for role in roles_data] if roles_data else [],
            "permissions": [format_permission_data(permission) for permission in permissions_data] if permissions_data else []
        }
    return None
