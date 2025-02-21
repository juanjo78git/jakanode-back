# pylint: disable=R0801
"""
Auth Providers Operations
"""

from database.db_config import (
    close_db_connection,
    commit_db_connection,
    get_db_connection,
)


def create_auth_provider(user_id, provider_name, provider_id):
    """
    Creates an authentication provider record for a user.

    Args:
        user_id (int): User ID.
        provider_name (str): Name of the provider (e.g., 'password', 'google', 'telegram').
        provider_id (str): Unique identifier for the provider.

    Returns:
        bool: True if creation was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO auth_providers (user_id, provider_name, provider_id)
        VALUES (?, ?, ?)
        """,
        (user_id, provider_name, provider_id),
    )

    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0


def delete_auth_providers_by_user(user_id):
    """
    Deletes all authentication provider records for a user.

    Args:
        user_id (int): ID of the user.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM auth_providers WHERE user_id = ?", (user_id,))
    commit_db_connection(connection)
    close_db_connection(connection)

    return cursor.rowcount > 0
