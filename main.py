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
from slowapi.errors import RateLimitExceeded

from app.api.routes import routers
from app.auth.telegram import router as telegram_auth_router
from app.core.cors import add_cors
from app.core.logging import logger
from app.core.rate_limit_exceptions import rate_limit_exceeded_handler
from app.core.rate_limiting import limiter
from app.core.security import SecurityHeadersMiddleware

app = FastAPI(
    title="Jakanode API",
    description="API providing public and private endpoints.",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

logger.debug(
    "Add Security Middleware to include HTTP security headers in every response."
)
app.add_middleware(SecurityHeadersMiddleware)

logger.debug("Adds CORS middleware to the FastAPI application.")
add_cors(app)

logger.debug("Set up the rate limiting.")
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.state.limiter = limiter  # Associate the limiter with the app

logger.debug("Include the Telegram authentication router.")
app.include_router(telegram_auth_router, prefix="/api/v1", tags=["Authentication"])

logger.debug("Include all routers from the routes package:")
for router_entry in routers:
    logger.debug(
        "Router: %s Prefix: %s Tags: %s",
        router_entry["router"],
        router_entry["prefix"],
        router_entry["tags"],
    )
    app.include_router(
        router_entry["router"], prefix=router_entry["prefix"], tags=router_entry["tags"]
    )

if __name__ == "__main__":
    import uvicorn

    logger.debug("Run uvicorn...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
