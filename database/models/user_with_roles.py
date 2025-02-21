# pylint: disable=R0801
"""
User with Roles Model
"""

from database.models.roles import format_role_data
from database.models.users import format_user_data


def format_user_with_roles(user_data, roles_data):
    """
    Formats user data including their roles.

    Args:
        user_data (tuple): User data from the database.
        roles_data (list of tuples): List of roles assigned to the user.

    Returns:
        dict: A dictionary containing user data and their roles.
    """
    if user_data:
        return {
            "user": format_user_data(user_data),
            "roles": (
                [format_role_data(role) for role in roles_data] if roles_data else []
            ),
        }
    return None
