"""
User Model
"""


def format_user_data(user_data):
    """
    Formats the user data.

    Args:
        user_data (tuple): A tuple containing the user's data from the database.

    Returns:
        dict: A dictionary with the formatted user data or None if no data is provided.
    """
    if user_data:
        return {
            "id": user_data[0],
            "email": user_data[1],
            "password_hash": user_data[2],
            "password_salt": user_data[3],
            "full_name": user_data[4],
            "language": user_data[5],
            "status": user_data[6],
            "failed_attempts": user_data[7],
            "last_failed_attempt": user_data[8],
            "created_at": user_data[9],
            "updated_at": user_data[10],
        }
    return None
