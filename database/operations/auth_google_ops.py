"""
Google Authentication Operations
"""

from database.db_config import (
    close_db_connection,
    commit_db_connection,
    get_db_connection,
)


def create_auth_google(user_id, google_id, email, full_name, profile_picture=None):
    """
    Creates a Google authentication record for a user.

    Args:
        user_id (int): ID of the user.
        google_id (str): Google account ID.
        email (str): Email address.
        full_name (str): Full name of the user.
        profile_picture (str, optional): URL of the profile picture.

    Returns:
        bool: True if creation was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO auth_google (user_id, google_id, email, full_name, profile_picture)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, google_id, email, full_name, profile_picture),
    )

    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0


def get_auth_google_by_user(user_id):
    """
    Retrieves Google authentication details by user ID.

    Args:
        user_id (int): User ID.

    Returns:
        tuple: Google authentication data or None.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM auth_google WHERE user_id = ?", (user_id,))
    auth_data = cursor.fetchone()

    close_db_connection(connection)
    return auth_data


def delete_auth_google_by_user(user_id):
    """
    Deletes Google authentication data for a user.

    Args:
        user_id (int): ID of the user.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM auth_google WHERE user_id = ?", (user_id,))
    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0
