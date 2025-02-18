"""
Security Headers Middleware for FastAPI

This middleware adds security-related HTTP headers to all responses,
helping to protect the application against various web vulnerabilities,
such as MIME-type sniffing, clickjacking, and cross-site scripting (XSS).

Headers included:
- X-Content-Type-Options: Prevents MIME-type sniffing.
- X-Frame-Options: Prevents embedding in iframes (clickjacking protection).
- X-XSS-Protection: Enables browser XSS filtering.
- Strict-Transport-Security: Enforces HTTPS (HSTS).
"""

from typing import Awaitable, Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds security-related HTTP headers to each response.
    These headers help protect against various web vulnerabilities.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """
        Process the incoming request, add security headers to the response,
        and return the modified response.

        Parameters:
            request (Request): The incoming HTTP request object.
            call_next (Callable): A function that takes the request as a parameter
                                  and returns an HTTP Response.

        Returns:
            Response: The HTTP response with additional security headers.

        Raises:
            Exception: Propagates any exception raised during the processing of the request.
        """
        # Process the incoming request and obtain the response
        response: Response = await call_next(request)

        # Add security headers to the response

        # Prevents browsers from guessing the MIME type, mitigating MIME-sniffing attacks.
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevents the page from being displayed in a frame, protecting against clickjacking.
        response.headers["X-Frame-Options"] = "DENY"

        # Enables the browser's XSS protection and instructs it to block the response if an attack is detected.
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Enforces HTTPS by telling browsers to only connect via HTTPS for the next 31536000 seconds (1 year)
        # and includes all subdomains.
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

        # Content-Security-Policy (CSP) + Swagger UI
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-eval' 'unsafe-inline' cdn.jsdelivr.net unpkg.com; "
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net unpkg.com; "
            "font-src 'self' cdn.jsdelivr.net;"
        )
        response.headers["X-Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-eval' 'unsafe-inline' cdn.jsdelivr.net unpkg.com; "
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net unpkg.com; "
            "font-src 'self' cdn.jsdelivr.net;"
        )

        # Referrer Policy
        response.headers["Referrer-Policy"] = "no-referrer"

        # Permissions Policy
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"

        # Prevent caching of sensitive data
        response.headers["Cache-Control"] = "no-store"

        # Expect-CT (optional)
        response.headers["Expect-CT"] = (
            "max-age=86400, enforce, report-uri='https://example.com/report'"
        )

        return response
