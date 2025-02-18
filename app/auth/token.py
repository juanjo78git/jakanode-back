"""
JWT Token Utilities

This module provides functions to create and manage JWT tokens
for authenticating users in the application.
"""

from datetime import datetime, timedelta

from jose import jwt  # Using python-jose for JWT handling

from app.core.settings import ALGORITHM, SECRET_KEY


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """
    Generates a JWT access token with an expiration time.

    Args:
        data (dict): The data to encode in the token (e.g., user identifier).
        expires_delta (timedelta): The duration for which the token is valid.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
