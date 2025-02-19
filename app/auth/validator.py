"""
Validator for Telegram authentication data.

This module provides functions to validate the authentication data
received from the Telegram login widget.
"""

import hashlib
import hmac
import time

from app.core.logging import logger
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
    try:
        logger.debug("Received authentication data: %s", data)
        # Convert auth_date to an integer and check if the data is not too old.
        auth_date = data.get("auth_date")
        if not auth_date:
            logger.error("Missing 'auth_date' in authentication data.")
            return False

        try:
            auth_date = int(auth_date)
        except ValueError:
            logger.error("Invalid 'auth_date' format: %s", auth_date)
            return False
        current_time = int(time.time())

        # If the authentication data is older than 60 seconds, consider it expired.
        if current_time - auth_date > 60:
            logger.error(
                "Authentication data expired: current_time - auth_date = %s",
                current_time - auth_date,
            )
            return False

        # Retrieve the provided hash. If not present, log and return False.
        provided_hash = data.get("hash")
        if provided_hash is None:
            logger.error("No hash provided in authentication data.")
            return False

        # Build the data string by sorting the parameters and excluding keys with None and 'hash'.
        data_str = "\n".join(
            f"{k}={v}" for k, v in sorted(data.items()) if k != "hash" and v is not None
        )

        # Create a secret key from the Telegram bot token.
        secret_key = hashlib.sha256(TELEGRAM_BOT_TOKEN.encode()).digest()

        # Calculate the hash using HMAC with SHA256.
        calculated_hash = hmac.new(
            secret_key, data_str.encode(), hashlib.sha256
        ).hexdigest()

        logger.debug("Data string used for hash calculation: %s", data_str)
        logger.debug(
            "Generated secret key (SHA-256 of bot token): %s", secret_key.hex()
        )
        logger.debug("Provided hash: %s", provided_hash)
        logger.debug("Calculated hash: %s", calculated_hash)

        # Securely compare the provided hash with the calculated hash.
        if hmac.compare_digest(provided_hash, calculated_hash):
            logger.info("Telegram authentication successful.")
            return True

        logger.error("Error: Hash mismatch! Authentication failed.")

    except (ValueError, KeyError, TypeError) as e:
        logger.error(
            "Error during Telegram authentication verification: %s", e, exc_info=True
        )
    return False
