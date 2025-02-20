"""
Role Permissions Model
"""

def format_role_permission_data(role_permission_data):
    """
    Formats role permission data.

    Args:
        role_permission_data (tuple): Tuple with role permission data from the database.

    Returns:
        dict: Formatted role permission data or None if no data is provided.
    """
    if role_permission_data:
        return {
            "id": role_permission_data[0],
            "role_id": role_permission_data[1],
            "permission_id": role_permission_data[2],
            "created_at": role_permission_data[3],
            "updated_at": role_permission_data[4],
        }
    return None
