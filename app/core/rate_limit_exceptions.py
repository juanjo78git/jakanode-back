"""
Rate Limit Exceeded Exception Handler

This module defines a custom exception handler for handling rate limiting errors
in the application. It specifically handles the RateLimitExceeded exception raised
when a client exceeds the allowed number of requests.

Functionality:
- Provides a custom handler for the 429 RateLimitExceeded error.

The handler responds with a custom message when a rate limit is exceeded.
"""

from fastapi import Request, Response
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


async def rate_limit_exceeded_handler(request: Request, exc: Exception) -> Response:
    """
    Custom handler for the rate limit exceeded error (429).

    Args:
        request (Request): The incoming HTTP request that caused the error.
        exc (Exception): The exception instance triggered by exceeding rate limits.

    Returns:
        Response: A custom response indicating the rate limit has been exceeded.
    """
    if isinstance(exc, RateLimitExceeded):  # ✅ Verifica si es un RateLimitExceeded
        return _rate_limit_exceeded_handler(request, exc)

    raise exc
