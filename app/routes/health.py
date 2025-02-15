from fastapi import APIRouter

router = APIRouter()

@router.get("/health", summary="Health Check", description="Returns API health status.")
async def health_check():
    """
    Health check endpoint to verify if the API is running.
    
    Returns:
        JSON object with a status message.
    """
    return {"status": "ok"}

