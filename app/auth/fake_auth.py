"""
Fake Authentication Middleware for FastAPI

This module provides a simulated authentication mechanism for testing purposes.
It verifies the presence and validity of an authorization token in the request headers.
If authentication fails, an HTTP 401 Unauthorized error is returned.

Authentication Process:
- The client must include an `Authorization` header in the format: `Bearer secret_token`.
- If the token is missing or incorrect, access is denied.
- If valid, the function returns a mock user dictionary.

Note: This is a placeholder authentication function and should be replaced
with a real authentication mechanism in production (e.g., OAuth2, JWT).
"""

from fastapi import Header, HTTPException, status

from app.core.logging import logger


def fake_auth(authorization: str = Header(None)):
    """
    Simulated authentication function.

    This function extracts and validates an authentication token from
    the HTTP request headers. It ensures that only authorized users
    can access protected endpoints.

    Parameters:
        authorization (str): The `Authorization` header containing the token.
                             Expected format: `Bearer secret_token`.

    Returns:
        dict: A dictionary containing mock user information.

    Raises:
        HTTPException:
            - 401 Unauthorized if the `Authorization` header is missing.
            - 401 Unauthorized if the token is invalid.
    """
    if not authorization:
        logger.warning("Authentication failed: Missing token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
        )

    # Extract token from the Authorization header (format: "Bearer secret_token")
    token = authorization.split(" ")[1] if " " in authorization else authorization

    if token != "secret_token":
        logger.warning(f"Authentication failed: Invalid token '{token}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    logger.info("Authentication successful for user 'demo'")
    return {"user": "demo"}
