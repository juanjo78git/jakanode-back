"""
User with Authentication Methods Model
"""

from database.models.users import format_user_data
from database.models.auth_telegram import format_telegram_data
from database.models.auth_google import format_google_data
from database.models.auth_providers import format_auth_provider_data

def format_user_with_auths(user_data, telegram_data=None, google_data=None, auth_providers=None):
    """
    Formats a full user record, including authentication methods.

    Args:
        user_data (tuple): User data from the database.
        telegram_data (tuple, optional): Telegram authentication data.
        google_data (tuple, optional): Google authentication data.
        auth_providers (list of tuples, optional): List of authentication providers.

    Returns:
        dict: A dictionary with user details and linked authentication methods.
    """
    if user_data:
        return {
            "user": format_user_data(user_data),
            "auth_methods": {
                "telegram": format_telegram_data(telegram_data) if telegram_data else None,
                "google": format_google_data(google_data) if google_data else None,
                "providers": [format_auth_provider_data(p) for p in auth_providers] if auth_providers else []
            }
        }
    return None
