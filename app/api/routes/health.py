"""
Health Check Route for FastAPI

This module defines an endpoint for monitoring the health status of the API.
It can be used to verify if the server is running and responding properly.

Endpoint:
- `/health` (Health Check): Returns a status message indicating API health.

This route is useful for uptime monitoring, automated health checks,
and ensuring system availability.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Health Check", description="Returns API health status.")
async def health_check():
    """
    Health check endpoint to verify if the API is running.

    Returns:
        dict: A JSON object with a status message.
    """
    return {"status": "ok"}
