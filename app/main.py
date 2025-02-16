from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import public, private, health
from starlette.middleware.base import BaseHTTPMiddleware

# Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

app = FastAPI(
        title="Jakanode API",
        description="API providing public and private endpoints.",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs", 
        redoc_url="/api/v1/redoc"
      )
# CORS
origins = [
    "https://jakanode.freeddns.org",
    "http://localhost",
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)
# Security Middleware
app.add_middleware(SecurityHeadersMiddleware)

# API Routes
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(public.router, prefix="/api/v1", tags=["Public"])
app.include_router(private.router, prefix="/api/v1", tags=["Private"])

