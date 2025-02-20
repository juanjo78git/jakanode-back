"""
Auth Providers Model
"""

def format_auth_provider_data(provider_data):
    """
    Formats authentication provider data.

    Args:
        provider_data (tuple): Tuple with provider data from the database.

    Returns:
        dict: Formatted provider data or None if no data is provided.
    """
    if provider_data:
        return {
            "id": provider_data[0],
            "user_id": provider_data[1],
            "provider": provider_data[2],  # 'telegram', 'google', 'password'
            "provider_id": provider_data[3],  # Telegram ID, Google ID or None
            "last_login": provider_data[4],
            "linked_user_id": provider_data[5],
            "created_at": provider_data[6],
            "updated_at": provider_data[7],
        }
    return None
