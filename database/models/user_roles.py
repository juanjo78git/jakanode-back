"""
User Roles Model
"""

def format_user_role_data(user_role_data):
    """
    Formats user role data.

    Args:
        user_role_data (tuple): Tuple with user role data from the database.

    Returns:
        dict: Formatted user role data or None if no data is provided.
    """
    if user_role_data:
        return {
            "id": user_role_data[0],
            "user_id": user_role_data[1],
            "role_id": user_role_data[2],
            "created_at": user_role_data[3],
            "updated_at": user_role_data[4],
        }
    return None
