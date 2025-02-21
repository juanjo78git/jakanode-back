# pylint: disable=R0801
"""
Telegram Authentication Operations
"""

from database.db_config import (
    close_db_connection,
    commit_db_connection,
    get_db_connection,
)


def create_auth_telegram(
    user_id, telegram_id, first_name, *, last_name=None, username=None, photo_url=None
):
    """
    Creates a Telegram authentication record for a user.

    Args:
        user_id (int): ID of the user.
        telegram_id (int): Telegram ID.
        first_name (str): First name.
        last_name (str, optional): Last name.
        username (str, optional): Telegram username.
        photo_url (str, optional): Profile picture URL.

    Returns:
        bool: True if creation was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO auth_telegram (user_id, telegram_id, first_name, last_name, username, photo_url)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (user_id, telegram_id, first_name, last_name, username, photo_url),
    )

    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0


def get_auth_telegram_by_user(user_id):
    """
    Retrieves Telegram authentication details by user ID.

    Args:
        user_id (int): User ID.

    Returns:
        tuple: Telegram authentication data or None.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM auth_telegram WHERE user_id = ?", (user_id,))
    auth_data = cursor.fetchone()

    close_db_connection(connection)
    return auth_data


def delete_auth_telegram_by_user(user_id):
    """
    Deletes Telegram authentication data for a user.

    Args:
        user_id (int): ID of the user.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM auth_telegram WHERE user_id = ?", (user_id,))
    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0
