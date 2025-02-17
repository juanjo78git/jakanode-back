"""
Main application entry point for the Jakanode API.

This module creates the FastAPI application instance, configures global
security and CORS settings, and mounts the various API routers (health,
public, and private endpoints) under the /api/v1 prefix.

Endpoints:
    - /api/v1/health: Health check endpoint.
    - /api/v1/ (and subpaths): Public endpoints.
    - /api/v1/ (and subpaths): Private endpoints (require authentication).

Security:
    - Adds security headers to each response via SecurityHeadersMiddleware.
    - Configures Cross-Origin Resource Sharing (CORS) using a helper function.

Documentation:
    - OpenAPI schema is available at /api/v1/openapi.json.
    - Swagger UI is available at /api/v1/docs.
    - ReDoc is available at /api/v1/redoc.
"""

from fastapi import FastAPI

from app.api.routes import health, private, public
from app.core.config import add_cors
from app.core.rate_limiting import _rate_limit_exceeded_handler, limiter
from app.core.security import SecurityHeadersMiddleware

app = FastAPI(
    title="Jakanode API",
    description="API providing public and private endpoints.",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# Add Security Middleware to include HTTP security headers in every response.
app.add_middleware(SecurityHeadersMiddleware)

# Configure Cross-Origin Resource Sharing (CORS) settings.
add_cors(app)

# Set up the rate limiting exception handler
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.state.limiter = limiter  # Associate the limiter with the app

# Include API routes with the /api/v1 prefix and appropriate tags for documentation.
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(public.router, prefix="/api/v1", tags=["Public"])
app.include_router(private.router, prefix="/api/v1", tags=["Private"])
