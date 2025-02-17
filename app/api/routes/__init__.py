"""
This package contains all the API route modules for the application.

It aggregates the different route definitions (public, private, health, etc.)
to facilitate their import from a single module.

Available routers:
    - public_router: Contains public endpoints.
    - private_router: Contains endpoints that require authentication.
    - health_router: Contains endpoints for health checks.
"""

from app.api.routes import health, private, public

# List of all routers to be included in the main FastAPI application
routers = [
    {"router": health.router, "prefix": "/api/v1", "tags": ["Health"]},
    {"router": public.router, "prefix": "/api/v1", "tags": ["Public"]},
    {"router": private.router, "prefix": "/api/v1", "tags": ["Private"]},
]

# Expose only the routers variable when importing this package
__all__ = ["routers"]
