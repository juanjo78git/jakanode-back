"""
Validator for Telegram authentication data.

This module provides functions to validate the authentication data
received from the Telegram login widget.
"""

import hashlib
import hmac
import time

from app.core.settings import TELEGRAM_BOT_TOKEN


def check_telegram_auth(data: dict) -> bool:
    """
    Verifies the Telegram authentication data using the bot token.

    Args:
        data (dict): A dictionary containing authentication parameters
                     from Telegram (e.g., id, first_name, auth_date, hash, etc.).

    Returns:
        bool: True if the authentication data is valid, False otherwise.
    """
    # Convert auth_date to integer and check if the data is not too old
    auth_date = int(data.get("auth_date", 0))
    current_time = int(time.time())

    # If the authentication data is older than 60 seconds, consider it expired
    if current_time - auth_date > 60:
        return False

    # Extract the hash and prepare the data string for verification
    check_hash = data.pop("hash", None)
    data_str = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))

    # Create a secret key from the Telegram bot token
    secret_key = hashlib.sha256(TELEGRAM_BOT_TOKEN.encode()).digest()

    # Calculate the hash using HMAC with SHA256
    calculated_hash = hmac.new(
        secret_key, data_str.encode(), hashlib.sha256
    ).hexdigest()

    # Compare the provided hash with the calculated one
    return hmac.compare_digest(check_hash, calculated_hash)
