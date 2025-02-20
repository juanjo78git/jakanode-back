"""
Roles Model
"""

def format_role_data(role_data):
    """
    Formats role data.

    Args:
        role_data (tuple): Tuple with role data from the database.

    Returns:
        dict: Formatted role data or None if no data is provided.
    """
    if role_data:
        return {
            "id": role_data[0],
            "name": role_data[1],
            "description": role_data[2],
            "created_at": role_data[3],
            "updated_at": role_data[4],
        }
    return None
