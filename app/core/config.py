"""
CORS Middleware Configuration for FastAPI

This module configures Cross-Origin Resource Sharing (CORS) middleware
to allow controlled access to the API from specified origins. CORS is
necessary for enabling web applications hosted on different domains
to interact with the API securely.

Allowed Origins:
- https://jakanode.freeddns.org (Production API access)
- http://localhost (General local development)
- http://localhost:4200 (Angular development server)

CORS Configuration:
- allow_credentials: Allows credentials (cookies, authorization headers, etc.).
- allow_methods: Specifies allowed HTTP methods (GET, POST, PUT, DELETE).
- allow_headers: Specifies allowed headers (Authorization, Content-Type).
"""

from fastapi.middleware.cors import CORSMiddleware

# List of allowed origins for CORS
origins = [
    "https://jakanode.freeddns.org",  # Production API access
    "http://localhost",  # Local development
    "http://localhost:4200",  # Angular development server
]


def add_cors(app):
    """
    Adds CORS middleware to the FastAPI application.

    This function enables CORS for the specified origins, allowing
    cross-origin requests with credentials, and restricting allowed
    HTTP methods and headers.

    Parameters:
        app (FastAPI): The FastAPI application instance.

    Raises:
        Exception: If the middleware cannot be added due to an internal error.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # List of allowed origins
        allow_credentials=True,  # Allow cookies, authentication headers, etc.
        allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allowed HTTP methods
        allow_headers=["Authorization", "Content-Type"],  # Allowed HTTP headers
    )
