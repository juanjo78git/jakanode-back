"""
Telegram Authentication Module for FastAPI

This module provides authentication functionality for the FastAPI application.
It allows authentication using either:
  - A simulated method (`fake_auth`) for testing purposes.
  - A real JWT verification (`verify_telegram_token`) for users authenticated via Telegram.

Functions:
    - combined_auth: Determines whether to authenticate using `fake_auth` or `verify_telegram_token`.
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth.fake_auth import fake_auth  # Your existing fake_auth function
from app.auth.telegram_auth import (
    verify_telegram_token,
)  # Your function that verifies the JWT

# Define the OAuth2 scheme to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/telegram")


def combined_auth(token: str = Depends(oauth2_scheme)):
    """
    Combined authentication dependency that verifies the token using either a simulated
    method (fake_auth) or real JWT verification (verify_telegram_token).

    The function reuses the existing implementations:
      - If the token is exactly "secret_token", it delegates to fake_auth.
      - Otherwise, it uses verify_telegram_token to decode and validate the JWT.

    Args:
        token (str): The token extracted from the Authorization header.

    Returns:
        dict: A dictionary containing the authenticated user's information.

    Raises:
        HTTPException: If the token is missing or invalid.
    """
    # If the token is the simulated one, use fake_auth
    if token == "secret_token":
        # Call fake_auth, passing the token as the header value
        return fake_auth(authorization=token)
    # Otherwise, use real JWT verification
    return verify_telegram_token(token)
