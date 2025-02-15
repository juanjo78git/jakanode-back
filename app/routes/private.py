from fastapi import APIRouter, Depends, HTTPException, status, Header

router = APIRouter()

def fake_auth(authorization: str = Header(None)):
    """
    Simulated authentication function.

    Args:
        authorization (str): The Authorization header containing the token.

    Raises:
        HTTPException: 401 Unauthorized if the token is missing or invalid.

    Returns:
        dict: A dictionary containing user information.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
        )

    # Header Authorization "Bearer secret_token"
    token = authorization.split(" ")[1] if " " in authorization else authorization
    if token != "secret_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return {"user": "demo"}

@router.get("/dashboard", summary="User Dashboard", description="Accessible only by authenticated users.")
async def dashboard(user: dict = Depends(fake_auth)):
    """
    Dashboard endpoint for authenticated users.

    Requires a valid Authorization token.

    Returns:
        JSON object with a welcome message for the user.
    """
    return {"message": f"Hello, {user['user']}"}

@router.get("/admin", summary="Admin Panel", description="Restricted to authenticated users.")
async def admin(user: dict = Depends(fake_auth)):
    """
    Admin panel endpoint.

    Requires a valid Authorization token.

    Returns:
        JSON object indicating admin access.
    """
    return {"message": f"Admin panel for {user['user']}"}

