"""
Telegram Authentication Model
"""


def format_telegram_data(telegram_data):
    """
    Formats Telegram authentication data.

    Args:
        telegram_data (tuple): Tuple with Telegram data from the database.

    Returns:
        dict: Formatted Telegram data or None if no data is provided.
    """
    if telegram_data:
        return {
            "id": telegram_data[0],
            "user_id": telegram_data[1],
            "telegram_id": telegram_data[2],
            "username": telegram_data[3],
            "first_name": telegram_data[4],
            "last_name": telegram_data[5],
            "photo_url": telegram_data[6],
            "created_at": telegram_data[7],
            "updated_at": telegram_data[8],
        }
    return None
