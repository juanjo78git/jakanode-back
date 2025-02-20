"""
Google Authentication Model
"""


def format_google_data(google_data):
    """
    Formats Google authentication data.

    Args:
        google_data (tuple): Tuple with Google data from the database.

    Returns:
        dict: Formatted Google data or None if no data is provided.
    """
    if google_data:
        return {
            "id": google_data[0],
            "user_id": google_data[1],
            "google_id": google_data[2],
            "full_name": google_data[3],
            "email": google_data[4],
            "picture": google_data[5],
            "created_at": google_data[6],
            "updated_at": google_data[7],
        }
    return None
