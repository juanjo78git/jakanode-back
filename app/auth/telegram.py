"""
Telegram Authentication Router

This module defines the API endpoint for authenticating users via Telegram.
It validates the authentication data received from Telegram and issues a JWT token.
"""

from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.token import create_access_token
from app.auth.validator import check_telegram_auth
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@dataclass
class TelegramAuthData:
    """
    Class to store the Telegram authentication data.

    This class represents the necessary fields to authenticate a user via Telegram's login widget.
    """

    telegram_id: str
    auth_date: str
    auth_hash: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None


@router.get("/auth/telegram")
def authenticate_via_telegram(
    telegram_data: TelegramAuthData = Depends(TelegramAuthData),
):
    """
    Endpoint to authenticate users via the Telegram login widget.

    This endpoint receives authentication data from Telegram as query parameters,
    verifies the data, and returns a JWT token if valid.

    Query Parameters:
        id (str): Telegram user ID.
        first_name (str, optional): User's first name.
        last_name (str, optional): User's last name.
        username (str, optional): Telegram username.
        photo_url (str, optional): URL to the user's profile photo.
        auth_date (str): Timestamp when the authentication was initiated.
        hash (str): The hash provided by Telegram for verification.

    Returns:
        dict: A JSON object with the access token and token type.
    """
    user_data = telegram_data.__dict__

    if not check_telegram_auth(user_data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid authentication data",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(telegram_data.telegram_id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
