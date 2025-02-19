"""
Telegram Authentication Router

This module defines the API endpoint for authenticating users via Telegram.
It receives the authentication data from the Telegram Login Widget, validates it,
and if valid, issues a JWT token for the user.

Authentication flow:
1. The frontend uses the Telegram Login Widget to obtain authentication data.
2. The frontend sends this data to the `/auth/telegram` API endpoint.
3. The backend validates the data, generates a JWT token if valid, and returns it.
4. The frontend stores and uses the JWT token for subsequent authenticated API requests.
"""

from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.auth.schemas.auth import TokenSchema
from app.auth.token import create_access_token
from app.auth.validator import check_telegram_auth
from app.core.logging import logger
from app.core.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@dataclass
class TelegramAuthData(BaseModel):
    """
    Stores the authentication data received from Telegram's Login Widget.

    This class represents the necessary fields to authenticate a user using Telegram's
    authentication system via the Telegram Login Widget.
    """

    id: int  # Telegram user ID (unique identifier for each user)
    auth_date: int  # Timestamp of when the user authenticated (in Unix format)
    hash: str  # Authentication hash provided by Telegram for verification
    first_name: Optional[str] = None  # User's first name (optional)
    last_name: Optional[str] = None  # User's last name (optional)
    username: Optional[str] = None  # Telegram username (optional)
    photo_url: Optional[str] = None  # URL to user's profile photo (optional)


@router.post(
    "/auth/telegram",
    summary="Authenticate user via Telegram",
    description=(
        "This endpoint receives authentication data from Telegram's Login Widget, "
        "validates it using the bot token, and returns a JWT token if the data is valid."
    ),
    response_model=TokenSchema,  # Response schema to define the structure of the returned token
    tags=["Authentication"],
)
def authenticate_via_telegram(telegram_data: TelegramAuthData):
    """
    Endpoint to authenticate users via Telegram login widget.

    This API endpoint receives authentication data as parameters from Telegram,
    verifies the authenticity of the data, and returns a JWT token if the data is valid.

    Query Parameters (all optional except `id`, `auth_date`, and `hash`):
    - **id (int)**: Unique Telegram user ID.
    - **auth_date (int)**: The timestamp (in Unix format) when authentication occurred.
    - **hash (str)**: The hash provided by Telegram for data validation.
    - **first_name (str, optional)**: The user's first name.
    - **last_name (str, optional)**: The user's last name.
    - **username (str, optional)**: The Telegram username.
    - **photo_url (str, optional)**: URL to user's profile photo.

    Returns:
    - **access_token (str)**: A JWT token that should be used for subsequent authenticated requests.
    - **token_type (str)**: The type of the token (usually "bearer").

    Raises:
    - **400 Bad Request**: If the authentication data is invalid or expired.
    """
    logger.debug("Received authentication request from Telegram: %s", telegram_data)

    # Extracting the authentication data to verify
    user_data = telegram_data.__dict__

    # Verifying the Telegram authentication data
    if not check_telegram_auth(user_data):
        logger.warning(f"Authentication failed for user ID: {telegram_data.id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid authentication data",  # Inform the client that data is invalid
        )

    # If authentication is successful, proceed with JWT token creation
    logger.info(f"User {telegram_data.id} authenticated successfully")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(telegram_data.id)}, expires_delta=access_token_expires
    )

    logger.debug(f"Generated access token for user {telegram_data.id}")
    return TokenSchema(
        access_token=access_token, token_type="bearer"
    )  # Returning the JWT token
