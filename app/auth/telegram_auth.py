"""
Telegram Authentication Token Verification for FastAPI

This module provides a dependency function to verify JWT tokens issued
after Telegram authentication. It ensures that only users with valid
authentication tokens can access protected endpoints.

Key Features:
- Uses OAuth2PasswordBearer to extract the token from requests.
- Decodes and validates the JWT using the configured secret key and algorithm.
- Extracts the user ID from the token payload.
- Raises an HTTP 401 error if the token is invalid or expired.

Usage:
This module should be used as a FastAPI dependency in protected endpoints
that require Telegram authentication.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.settings import ALGORITHM, SECRET_KEY

# Define the OAuth2 scheme with the token URL for Telegram authentication.
# This tells FastAPI where to obtain the token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/telegram")


def verify_telegram_token(token: str = Depends(oauth2_scheme)):
    """
    Dependency that verifies the JWT token issued after Telegram authentication.

    Args:
        token (str): The JWT token extracted from the Authorization header.

    Returns:
        dict: The decoded token payload, typically containing the user ID.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc
    return {"user": user_id}
