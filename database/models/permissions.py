"""
Permissions Model
"""


def format_permission_data(permission_data):
    """
    Formats permission data.

    Args:
        permission_data (tuple): Tuple with permission data from the database.

    Returns:
        dict: Formatted permission data or None if no data is provided.
    """
    if permission_data:
        return {
            "id": permission_data[0],
            "name": permission_data[1],
            "description": permission_data[2],
            "created_at": permission_data[3],
            "updated_at": permission_data[4],
        }
    return None
