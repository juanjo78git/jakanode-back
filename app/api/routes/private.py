"""
Private Routes for FastAPI

This module defines endpoints that require authentication.
These endpoints are restricted to authenticated users and require a valid
Authorization token in the request header.

Endpoints:
- /dashboard: Returns a welcome message for authenticated users.
- /admin: Returns admin panel information for authenticated users.

Each endpoint uses the fake_auth dependency to simulate authentication.
Replace fake_auth with a real authentication mechanism in production.
"""

from fastapi import APIRouter, Depends

from app.auth.auth import fake_auth

router = APIRouter()


@router.get(
    "/dashboard",
    summary="User Dashboard",
    description="Accessible only by authenticated users.",
)
async def dashboard(user: dict = Depends(fake_auth)):
    """
    Dashboard endpoint for authenticated users.

    Requires:
        A valid Authorization token passed in the request header.

    Returns:
        dict: A JSON object with a welcome message for the authenticated user.

    Raises:
        HTTPException: 401 Unauthorized if the Authorization token is missing or invalid.
    """
    return {"message": f"Hello, {user['user']}"}


@router.get(
    "/admin", summary="Admin Panel", description="Restricted to authenticated users."
)
async def admin(user: dict = Depends(fake_auth)):
    """
    Admin panel endpoint.

    Requires:
        A valid Authorization token passed in the request header.

    Returns:
        dict: A JSON object indicating admin access for the authenticated user.

    Raises:
        HTTPException: 401 Unauthorized if the Authorization token is missing or invalid.
    """
    return {"message": f"Admin panel for {user['user']}"}
