"""
JWT Token Utilities

This module provides functions to create and manage JWT tokens
for authenticating users in the application.
"""

from datetime import datetime, timedelta

from jose import jwt  # Using python-jose for JWT handling

from app.core.logging import logger
from app.core.settings import ALGORITHM, SECRET_KEY


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """
    Generates a JWT access token with an expiration time.

    Args:
        data (dict): The data to encode in the token (e.g., user identifier).
        expires_delta (timedelta): The duration for which the token is valid.

    Returns:
        str: The encoded JWT token.

    Raises:
        Exception: Error generating JWT token
    """
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        logger.debug(
            f"JWT token created successfully for user: {data.get('sub')}, expires at {expire}"
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error generating JWT token: {e}")
        raise
