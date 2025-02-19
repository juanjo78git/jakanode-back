"""
Public Routes for FastAPI

This module defines public API endpoints that can be accessed without authentication.
These endpoints provide general information and a public home message.

Endpoints:
- `/` (Public Home): Returns a general public message.
- `/info` (Public Info): Provides general public information.

These routes can be accessed freely by any client.
"""

from fastapi import APIRouter, Request

from app.core.logging import logger
from app.core.rate_limiting import limiter

router = APIRouter()


@router.get(
    "/",
    summary="Public Home",
    description="Returns a message from the public home endpoint.",
)
@limiter.limit("5/minute")
# pylint: disable=W0613
async def home(request: Request):
    """
    Public home endpoint.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        dict: A JSON object containing a public message.
    """
    logger.debug("/ endpoint accessed successfully (public).")
    return {"message": "public route ok"}


@router.get("/info", summary="Public Info", description="Provides public information.")
@limiter.limit("5/minute")
# pylint: disable=W0613
async def info(request: Request):
    """
    Public information endpoint.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        dict: A JSON object containing public information.
    """
    logger.debug("/info endpoint accessed successfully (public).")
    return {"message": "Public info"}
