from fastapi import APIRouter

router = APIRouter()

@router.get("/", summary="Public Home", description="Returns a message from the public home endpoint.")
async def home():
    """
    Public home endpoint.
    
    Returns:
        JSON object with a public message.
    """
    return {"message": "public route ok"}

@router.get("/info", summary="Public Info", description="Provides public information.")
async def info():
    """
    Public information endpoint.
    
    Returns:
        JSON object with public information.
    """
    return {"message": "Public info"}

