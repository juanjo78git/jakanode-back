from fastapi import FastAPI
from app.routes import public, private, health

app = FastAPI(
        title= "Jakanode API",
        description="API Documentation",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs", 
        redoc_url="/api/v1/redoc"
      )

# API Routes
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(public.router, prefix="/api/v1", tags=["Public"])
app.include_router(private.router, prefix="/api/v1", tags=["Private"])
