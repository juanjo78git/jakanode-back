"""
Telegram Authentication Router

This module defines the API endpoint for authenticating users via Telegram.
It validates the authentication data received from Telegram and issues a JWT token.

The authentication process follows these steps:
1. The frontend uses the Telegram Login Widget to obtain authentication data.
2. The frontend sends this data to this API endpoint.
3. The API verifies the data and generates a JWT token if valid.
4. The client uses the JWT token for authenticated requests.
"""

from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.schemas.auth import TokenSchema
from app.auth.token import create_access_token
from app.auth.validator import check_telegram_auth
from app.core.logging import logger
from app.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@dataclass
class TelegramAuthData:
    """
    Stores Telegram authentication data.

    This class represents the required fields to authenticate a user via Telegram's login widget.
    """

    id: str  # Unique identifier for the Telegram user
    auth_date: str  # Timestamp of authentication
    hash: str  # Hash provided by Telegram for verification
    first_name: Optional[str] = None  # User's first name (optional)
    last_name: Optional[str] = None  # User's last name (optional)
    username: Optional[str] = None  # Telegram username (optional)
    photo_url: Optional[str] = None  # Profile photo URL (optional)


@router.get(
    "/auth/telegram",
    summary="Authenticate via Telegram",
    description=(
        "Authenticates users using the Telegram Login Widget. "
        "Receives authentication data, verifies it, and returns a JWT token."
    ),
    response_model=TokenSchema,  # Defines the expected response structure
    tags=["Authentication"],
)
def authenticate_via_telegram(
    telegram_data: TelegramAuthData = Depends(TelegramAuthData),
):
    """
    Authenticate users via the Telegram login widget.

    This endpoint receives authentication data from Telegram as query parameters,
    validates the data, and returns a JWT token if the authentication is successful.

    **Query Parameters:**
    - **id (str)**: The unique Telegram user ID.
    - **auth_date (str)**: The timestamp when authentication occurred.
    - **hash (str)**: The authentication hash provided by Telegram.
    - **first_name (str, optional)**: The user's first name.
    - **last_name (str, optional)**: The user's last name.
    - **username (str, optional)**: The Telegram username.
    - **photo_url (str, optional)**: The URL to the user's profile photo.

    **Returns:**
    - **access_token (str)**: The JWT token that should be used for subsequent authenticated requests.
    - **token_type (str)**: The token type (usually "bearer").

    **Raises:**
    - **400 Bad Request**: If the authentication data is invalid.
    """
    logger.debug(f"Received authentication request from Telegram: {telegram_data}")

    user_data = telegram_data.__dict__

    if not check_telegram_auth(user_data):
        logger.warning(f"Authentication failed for user ID: {telegram_data.id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid authentication data",
        )

    logger.info(f"User {telegram_data.id} authenticated successfully")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(telegram_data.id)}, expires_delta=access_token_expires
    )

    logger.debug(f"Generated access token for user {telegram_data.id}")
    return TokenSchema(access_token=access_token, token_type="bearer")
